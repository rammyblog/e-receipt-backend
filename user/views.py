from django.contrib.auth import get_user_model
from django.shortcuts import render
from djoser.compat import get_user_email
from djoser.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from djoser.conf import settings
from user.serializers import CustomTokenObtainPairSerializer
from djoser import signals
from rest_framework import serializers
from rest_framework.views import APIView

import cloudinary
import cloudinary.uploader
import cloudinary.api
user = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """
        post:
        Gives the access and refresh token
        The access token is used for authenticating the users
        * Authorization: Bearer access_token
        * Refresh tokens carry the information necessary to get a new access token
    """
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """
            post:
            Takes the refresh token gotten from jwt/token/create endpoint and gives a new access token
            The access token is used for authenticating the users
            * Authorization: Bearer access_token
                   The access token is used for authenticating the users
            * Authorization: Bearer access_token
            * Refresh tokens carry the information necessary to get a new access token
        """
    pass


class CustomUserViewSet(UserViewSet):
    # permission_classes = [IsAuthenticated]

    def custom_get_serializers_class(self):
        if self.action == "create":
            if settings.USER_CREATE_PASSWORD_RETYPE:
                return settings.SERIALIZERS.user_create_password_retype
            return settings.SERIALIZERS.user_create
        elif self.action == "destroy" or (
                self.action == "me" and self.request and self.request.method == "DELETE"
        ):
            return settings.SERIALIZERS.user_delete
        elif self.action == "activation":
            return settings.SERIALIZERS.activation
        elif self.action == "resend_activation":
            return settings.SERIALIZERS.password_reset
        elif self.action == "reset_password":
            return settings.SERIALIZERS.password_reset
        elif self.action == "reset_password_confirm":
            if settings.PASSWORD_RESET_CONFIRM_RETYPE:
                return settings.SERIALIZERS.password_reset_confirm_retype
            return settings.SERIALIZERS.password_reset_confirm
        elif self.action == "set_password":
            if settings.SET_PASSWORD_RETYPE:
                return settings.SERIALIZERS.set_password_retype
            return settings.SERIALIZERS.set_password
        elif self.action == "set_username":
            if settings.SET_USERNAME_RETYPE:
                return settings.SERIALIZERS.set_username_retype
            return settings.SERIALIZERS.set_username
        elif self.action == "reset_username":
            return settings.SERIALIZERS.username_reset
        elif self.action == "reset_username_confirm":
            if settings.USERNAME_RESET_CONFIRM_RETYPE:
                return settings.SERIALIZERS.username_reset_confirm_retype
            return settings.SERIALIZERS.username_reset_confirm
        elif self.action == "me":
            return settings.SERIALIZERS.current_user

        return self.serializer_class


    def perform_create(self, serializer):
        user = serializer.save().user
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )
        context = {"user": user}
        to = [get_user_email(user)]
        if settings.SEND_ACTIVATION_EMAIL:
            settings.EMAIL.activation(self.request, context).send(to)
        elif settings.SEND_CONFIRMATION_EMAIL:
            settings.EMAIL.confirmation(self.request, context).send(to)

    def perform_update(self, serializer):
        super().perform_update(serializer)
        user = serializer.instance
        # should we send activation email after update?
        if settings.SEND_ACTIVATION_EMAIL and not user.is_active:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.activation(self.request, context).send(to)



# class ImageUploadAPI(APIView):
#
#     def post(self, request):
#         if 'image' in request.FILES:
#             file_obj = request.FILES['image']
#             limit_mb = 5
#             file_size = file_obj.size
#             if file_size > limit_mb * 1024 * 1024:
#                 raise serializers.ValidationError(
#                     "Max size of file is %s MB" % limit_mb)
#
#             cloudinary_file = cloudinary.uploader.upload(
#                 file_obj, resource_type="raw")
#             # cloudinary_file['secure_url']