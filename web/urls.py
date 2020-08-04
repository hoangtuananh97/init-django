from django.urls import path, include

urlpatterns = [
    path('good/', include('web.api.goods.urls')),
]
