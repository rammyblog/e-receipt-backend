from random import choice
from string import digits

from django.contrib.auth import get_user_model

User = get_user_model()


def generate_random_username(chars, length=16, split=4, delimiter='-'):
    username = ''.join([choice(chars + digits) for i in range(length)])

    if split:
        username = delimiter.join([username[start:start + split] for start in range(0, len(username), split)])

    try:
        User.objects.get(username=username)
        return generate_random_username(length=length, chars=chars, split=split, delimiter=delimiter)
    except User.DoesNotExist:
        return username