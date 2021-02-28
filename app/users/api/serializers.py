from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core import exceptions
from django.db import transaction, IntegrityError
from djoser.conf import settings
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from app.users.models import UserProfile
from app.utils import error_json_render
from app.utils.fields import Base64ImageField

User = get_user_model()


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


class UserActivationSerializer(serializers.ModelSerializer):
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
            raise error_json_render.UserIsActivated

        is_token_valid = default_token_generator.check_token(
            self.user, self.initial_data.get("token", "")
        )
        if is_token_valid:
            return validated_data
        else:
            raise error_json_render.TokenInvalid


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            User._meta.pk.name,
            "password",
        )

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except exceptions.ValidationError as e:
            return error_json_render.NotMatchPassword

        return attrs

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            return error_json_render.IntegrityDataError
        return user

    def perform_create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save(update_fields=["is_active"])
        return user

    def to_representation(self, instance):
        data = super(UserCreateSerializer, self).to_representation(instance)
        del data['password']
        return data


class SendEmailSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.filter(email=email, is_active=True).first()
        if user:
            return email
        raise error_json_render.EmailNotFound


class UserProfileSerializerCreate(serializers.ModelSerializer):
    photo = Base64ImageField(use_url=True)
    address = serializers.CharField()
    phone = serializers.CharField()
    gender = serializers.IntegerField()

    class Meta:
        model = UserProfile
        fields = ['photo', 'address', 'phone', 'gender']

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        if not self.context['request'].user:
            raise error_json_render.LoginInvalid
        try:
            validated_data['user_id'] = self.context['request'].user.id
            return UserProfile.objects.create(**validated_data)
        except Exception as e:
            raise error_json_render.ServerDatabaseError


class UserProfileSerializerUpdate(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    photo = Base64ImageField(use_url=True, required=False)

    class Meta:
        model = UserProfile
        fields = ['id', 'photo', 'address', 'phone', 'gender']

    def validate(self, attrs):
        return attrs

    def update(self, instance, validated_data):
        print(123)
        return instance


class ListUserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    user_profile = UserProfileSerializer(read_only=True, source='user_relate_profile')

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'user_profile', 'date_joined']

    def get_fullname(self, obj):
        return '{first_name} {last_name}'.format(first_name=obj.first_name, last_name=obj.last_name)

    def get_user_profile(self, obj):
        return obj.user_relate_profile
