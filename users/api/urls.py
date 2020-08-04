from django.conf.urls import url

from users.api.views import UserRegistrationView, UserSigninView

urlpatterns = [
    url(r'^signup$', UserRegistrationView.as_view(), name='signup'),
    # url(r'^signin$', UserSigninView.as_view(), name='signin'),
]
