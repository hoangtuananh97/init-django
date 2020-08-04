from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from web.api.goods.serializers import ListGoodSerializer
from web.models import Good


class GoodSearch(ListAPIView):
    serializer_class = ListGoodSerializer
    # permission_classes = (AllowAny,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Good.objects.all()
