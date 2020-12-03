from django.urls import path, include

urlpatterns = [
    path('good/', include('app.web.api.goods.urls')),
]
