from uuid import uuid4

import boto3
from botocore.exceptions import ClientError
from django.db import DatabaseError
from djoser import utils
from djoser.compat import get_user_email
from djoser.conf import settings
from djoser.serializers import SendEmailResetSerializer
from rest_framework import generics, status, exceptions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from app.users.api.serializers import UserSigninSerializer, UserActivationSerializer, \
    UserCreateSerializer, SendEmailSerializer, ListUserSerializer, UserProfileSerializerCreate, \
    UserProfileSerializerUpdate
from app.users.models import User, UserProfile
from app.utils import error_json_render, signals
from app.utils.email import CustomActionEmail, RegisterComplete, SendMail
from config.settings.local import AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_REGION_NAME


class UserRegistrationView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = serializer.save()
                signals.user_registered.send(
                    sender=self.__class__,
                    user=user,
                    request=self.request
                )
                context = {"user": user}
                to = [get_user_email(user)]
                # send_email_ses()
                CustomActionEmail(self.request, context).send(to)
                return Response(status=status.HTTP_201_CREATED, data=serializer.data)
            except DatabaseError as e:
                return error_json_render.ServerDatabaseError
        raise error_json_render.BadRequestException


class UserSigninView(TokenViewBase):
    permission_classes = (AllowAny,)
    serializer_class = UserSigninSerializer


class UserActivationView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserActivationSerializer

    def post(self, request, *args, **kwargs):
        uid = kwargs['uid']
        try:
            pk = utils.decode_uid(uid)
            self.user = User.objects.get(pk=pk)
            kwargs['user'] = self.user
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise exceptions.NotFound(detail=f'User with id is {uid} not found!')

        serializer = self.get_serializer(data=kwargs)
        if serializer.is_valid(raise_exception=True):
            try:
                self.user.is_active = True
                self.user.save()
                data = serializer.data
                data['message'] = 'User is activated'
                signals.user_registered_complete.send(
                    sender=self.__class__,
                    user=self.user,
                    request=self.request
                )
                to = [get_user_email(self.user)]
                context = {"user": self.user}
                RegisterComplete(self.request, context).send(to)
                return Response(data=data, status=status.HTTP_204_NO_CONTENT)
            except DatabaseError as e:
                raise error_json_render.ServerDatabaseError
        return error_json_render.BadRequestException


class Logout(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh_token']
            RefreshToken(refresh_token).blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return error_json_render.BadRequestException


class SendEmailRestPassword(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SendEmailResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()

        if user:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.password_reset(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ForgotPassword(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SendEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = request.data['email']
            user = User.objects.filter(email=email).first()
            to = [user.email]
            context = {"user": user}
            SendMail(self.request, context).send(to)
            return Response(data={"Send mail": "Success"}, status=status.HTTP_204_NO_CONTENT)
        return error_json_render.BadRequestException


class UserProfileCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializerCreate

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return error_json_render.ServerDatabaseError


class UserProfileUpdate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializerUpdate

    def get_object(self):
        user = self.request.user
        if not user.is_active or user.is_deleted:
            raise error_json_render.UserIsActivatedOrIsDeleted
        try:
            return UserProfile.objects.get(id=user.id)
        except UserProfile.DoesNotExist:
            raise error_json_render.UserNotFound

    def delete(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serializer = self.get_serializer(user_profile, data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(serializer.data, status.HTTP_204_NO_CONTENT)
        raise error_json_render.BadRequestException


class SearchUser(generics.ListAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = ListUserSerializer

    def get_queryset(self):
        users = User.objects.select_related('user_relate_profile').all()

        return users


@api_view(['POST', 'PUT'])
@permission_classes((AllowAny,))
def create_presigned_post(object_name, fields=None, conditions=None, expiration=3600):
    session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3client = session.client('s3',
                              config=boto3.session.Config(signature_version='s3v4'),
                              region_name=AWS_S3_REGION_NAME)
    try:
        s3_object_name = str(uuid4()) + '.png'
        params = {
            "Key": 'hello.jpg',
            "Bucket": AWS_STORAGE_BUCKET_NAME,
            "ContentType": 'image/jpeg',
        }
        response = s3client.generate_presigned_url(ClientMethod="put_object",
                                                   Params=params,
                                                   ExpiresIn=3600)
        print("response", response)
        return Response({"presigned_post": response}, status=status.HTTP_200_OK)
    except ClientError as e:
        print(e)
