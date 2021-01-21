from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone_number = PhoneNumberField()
    username = models.CharField(unique=True, null=True, blank=True, max_length=150)
    address = models.CharField(null=True, blank=True, max_length=500)
    logo = models.URLField(max_length=500)

    def __str__(self):
        return self.email
