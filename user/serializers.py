from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from djoser.compat import get_user_email_field_name, get_user_email
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import PasswordField, TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from core.mixins.CustomErrorSerializer import CustomErrorSerializer
from user.utils.random_username import generate_random_username

User = get_user_model()


class CustomTokenObtainSerializer(TokenObtainSerializer, serializers.Serializer):
    email_field = User.EMAIL_FIELD
    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }

    def __init__(self, *args, **kwargs):
        super(serializers.Serializer, self).__init__(*args, **kwargs)
        # super().__init__(*args, **kwargs)
        self.fields[self.email_field] = serializers.EmailField()
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        try:
            username = User.objects.get(email=attrs[self.email_field]).username
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        authenticate_kwargs = {
            "username": username,
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)
        if self.user is None or not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        return {}


class CustomTokenObtainPairSerializer(CustomTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        # Add custom claims
        # token[f'{get_user_type(user)}_id'] = user.email
        # token['user_id'] = str(user.id)

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh_token'] = str(refresh)
        data['access_token'] = str(refresh.access_token)

        return data


class CustomUserCreateSerializer(CustomErrorSerializer, UserCreateSerializer):
    first_name = serializers.CharField(
        required=True)
    last_name = serializers.CharField(
        required=True)
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True, required=True)
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True, required=True)

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.DJOSER['LOGIN_FIELD'],
            'first_name',
            'last_name',
            "password",
            "confirm_password",
            "phone_number",
            "address",
            "logo"

        )
        extra_kwargs = {'logo': {'required': False}, 'email':{'required':True}}

    @staticmethod
    def validate_email(value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            return value
        raise serializers.ValidationError('Email already taken')

    def validate(self, attrs):
        password1 = attrs.get("password")
        password2 = attrs.get("confirm_password")

        if not password1:
            raise serializers.ValidationError('No password was provided')
        if not password2:
            raise serializers.ValidationError('Confirm password was not provided')
        if password1 != password2:
            raise serializers.ValidationError('The passwords does not match')

        return attrs

    def update(self, instance, validated_data):
        email_field = get_user_email_field_name(User)
        if settings.SEND_ACTIVATION_EMAIL and email_field in validated_data:
            instance_email = get_user_email(instance)
            if instance_email != validated_data[email_field]:
                instance.is_active = False
                instance.save(update_fields=["is_active"])

        return super().update(instance, validated_data)

    def perform_create(self, validated_data):
        validated_data['username'] = generate_random_username(
            chars=validated_data.get('first_name') + validated_data.get('last_name'))

        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            if settings.DJOSER['SEND_ACTIVATION_EMAIL']:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user


class CustomUserSerializer(CustomErrorSerializer, UserSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.DJOSER['LOGIN_FIELD'],
            'first_name',
            'last_name',
            "phone_number",
            "logo",
            "address"
        )
        read_only_fields = (settings.DJOSER['LOGIN_FIELD'],)
