from django.conf.urls import url
from django.urls import path

from app.users import views
from app.users.api.views import UserRegistrationView, UserSigninView

urlpatterns = [
    url(r'^signup$', UserRegistrationView.as_view(), name='signup'),
    url(r'^signin$', UserSigninView.as_view(), name='signin'),
]
