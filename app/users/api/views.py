from djoser import utils
from djoser.compat import get_user_email
from djoser.conf import settings
from djoser.serializers import SendEmailResetSerializer
from rest_framework import generics, status, exceptions
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from app.users.api.serializers import UserRegistrationSerializer, UserSigninSerializer, UserActivationSerializer
from app.users.models import User
from app.utils import error_json_render


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         self.perform_create(serializer)
    #     raise ErrorJsonRender.BadRequestException


class UserSigninView(TokenViewBase):
    permission_classes = (AllowAny,)
    serializer_class = UserSigninSerializer


class UserActivationView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserActivationSerializer

    def post(self, request, *args, **kwargs):
        try:
            uid = kwargs['uid']
            pk = utils.decode_uid(uid)
            self.user = User.objects.get(pk=pk)
            kwargs['user'] = self.user
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise exceptions.NotFound(detail=f'User with id is {uid} not found!')

        serializer = self.get_serializer(data=kwargs)
        if serializer.is_valid(raise_exception=True):
            self.user.is_active = True
            self.user.save()
            data = serializer.data
            data['message'] = 'User is actived'
            return Response(data=data, status=status.HTTP_200_OK)
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
