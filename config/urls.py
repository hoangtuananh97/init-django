"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView

from config import settings
from users.api.views import UserActivationView, Logout, SendEmailRestPassword

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('web.urls')),
    path('api/v1/', include('users.api.urls')),
    path('api/v1/auth/signin', TokenObtainPairView.as_view(), name='signin'),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/users/activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)$', UserActivationView.as_view()),
    url(r'^auth/users/reset_password$', SendEmailRestPassword.as_view()),
    url(r'^auth/users/reset_password_confirm$', SendEmailRestPassword.as_view()),
    url(r'^auth/users/logout$', Logout.as_view()),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
