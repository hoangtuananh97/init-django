from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from app.web.api.goods.serializers import ListGoodSerializer
from app.web.models import Good


class GoodSearch(ListAPIView):
    serializer_class = ListGoodSerializer
    # permission_classes = (AllowAny,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Good.objects.all()
