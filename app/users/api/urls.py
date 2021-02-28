from django.conf.urls import url

from app.users.api.views import UserRegistrationView, UserSigninView, UserActivationView, ForgotPassword, \
    UserProfileCreate, \
    SearchUser, UserProfileUpdate, create_presigned_post

urlpatterns = [
    url(r'^signup$', UserRegistrationView.as_view(), name='signup'),
    url(r'^signin$', UserSigninView.as_view(), name='signin'),
    url(r'^activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)$', UserActivationView.as_view(), name="activate"),
    url(r'^forgot-password$', ForgotPassword.as_view(), name="forgot_password"),
    url(r'^profile/create$', UserProfileCreate.as_view(), name="user_profile_create"),
    url(r'^profile/update$', UserProfileUpdate.as_view(), name="user_profile_update"),
    url(r'^search$', SearchUser.as_view(), name="search_user"),
    url(r'^presigned-url$', create_presigned_post, name="search_user"),
]
