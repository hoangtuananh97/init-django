from django.conf.urls import url

from app.web.api.goods.views import GoodSearch

urlpatterns = [
    url(r'^search$', GoodSearch.as_view(), name='goods_search'),
]

