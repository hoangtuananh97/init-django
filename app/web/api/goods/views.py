from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from app.utils import error_json_render
from app.web.api.goods.serializers import CommonGoodSerializer, CreateGoodSerializer, ListImageGood
from app.web.models import Good, ImageGood


class GoodSearch(ListAPIView):
    serializer_class = CommonGoodSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Good.objects.all()


class GoodCreateNew(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateGoodSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            data = serializer.data
            return Response(data=data, status=status.HTTP_201_CREATED)
        raise error_json_render.BadRequestException
