from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from djoser.conf import settings
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from app.users.models import UserProfile
from app.utils import ErrorJsonRender


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['address', 'photo', 'gender', 'phone']


# class UserRegistrationSerializer(serializers.ModelSerializer):
#     # profile = UserProfileSerializer(required=False)
#
#     class Meta:
#         model = User
#         fields = ['email', 'username', 'password']
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         # profile_data = validated_data.pop('profile')
#         user = User.objects.create_user(**validated_data)
#         # UserProfile.objects.create(
#         #     user=user,
#         #     phone=profile_data['phone'],
#         #     address=profile_data['address'],
#         #     gender=profile_data['gender']
#         # )
#         return user


class UserSigninSerializer(TokenObtainSerializer):

    def __init__(self, *args, **kwargs):
        if 'email' in kwargs['data']:
            self.username_field = 'email'
        super().__init__(*args, **kwargs)

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    # permission_classes = [AllowAny, ]

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def create(self, validated_data):
        with transaction.atomic():
            user = super(UserRegistrationSerializer, self).create(validated_data)
            user.save()
            return user

    def validate(self, attrs):
        return super(UserRegistrationSerializer, self).validate(self._kwargs['data'])

    def to_representation(self, instance):
        data = super(UserRegistrationSerializer, self).to_representation(instance)
        # refresh_token = self.get_token(instance)
        # data['access'] = str(refresh_token.access_token)
        return data


class UserActivationSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    default_error_messages = {
        "invalid_token": settings.CONSTANTS.messages.INVALID_TOKEN_ERROR,
        "invalid_uid": settings.CONSTANTS.messages.INVALID_UID_ERROR,
    }

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        self.user = self.initial_data.get("user", "")

        if self.user.is_active:
            raise ErrorJsonRender.UserIsActived

        is_token_valid = default_token_generator.check_token(
            self.user, self.initial_data.get("token", "")
        )
        if is_token_valid:
            return validated_data
        else:
            raise ErrorJsonRender.TokenInvalid
