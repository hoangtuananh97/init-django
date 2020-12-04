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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView

from app.users.api.views import UserActivationView, Logout, SendEmailRestPassword
from django.views import defaults as default_views

# CHECK HEALTHY
urlpatterns = [
    path('healthy/', TemplateView.as_view(template_name='healthy.html'), name='healthy'),
]

# PAGE ADMIN
urlpatterns += [
    path('admin/', admin.site.urls)
]

# API URLS
# djoser
urlpatterns += [
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/users/activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)$', UserActivationView.as_view()),
    url(r'^auth/users/reset_password$', SendEmailRestPassword.as_view()),
    url(r'^auth/users/reset_password_confirm$', SendEmailRestPassword.as_view()),
    url(r'^auth/users/logout$', Logout.as_view())
]

# API CUSTOM
# version api: api/v1
urlpatterns += [
    path('api/v1/web', include('app.web.urls')),
    path('api/v1/user/', include('app.users.api.urls')),
    path('api/v1/auth/signin', TokenObtainPairView.as_view(), name='signin')
]

# HANDLE PAGE ERROR
urlpatterns += [
    path(
        "400/",
        default_views.bad_request,
        kwargs={"exception": Exception("Bad Request!")},
    ),
    path(
        "403/",
        default_views.permission_denied,
        kwargs={"exception": Exception("Permission Denied")},
    ),
    path(
        "404/",
        default_views.page_not_found,
        kwargs={"exception": Exception("Page not Found")},
    ),
    path("500/", default_views.server_error),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
