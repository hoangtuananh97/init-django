from django.conf.urls import url

from app.web.api.goods.views import GoodSearch, GoodCreateNew

urlpatterns = [
    url(r'^search$', GoodSearch.as_view(), name='goods_search'),
    url(r'^create$', GoodCreateNew.as_view(), name='goods_create'),
]

