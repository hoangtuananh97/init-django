from django.conf.urls import url

from app.users.api.views import UserRegistrationView, UserSigninView, UserActivationView, ForgotPassword, UpdateUser

urlpatterns = [
    url(r'^signup$', UserRegistrationView.as_view(), name='signup'),
    url(r'^signin$', UserSigninView.as_view(), name='signin'),
    url(r'^activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)$', UserActivationView.as_view(), name="activate"),
    url(r'^forgot-password$', ForgotPassword.as_view(), name="forgot_password"),
    url(r'^update$', UpdateUser.as_view(), name="update_user"),
]
