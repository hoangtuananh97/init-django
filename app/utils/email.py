from django.contrib.auth.tokens import default_token_generator
from templated_mail.mail import BaseEmailMessage

from app.utils import utils


class CustomActionEmail(BaseEmailMessage):
    template_name = "mail/EmailActivation.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["url"] = 'api/v1/user/activate/{uid}/{token}'.format(uid=utils.encode_uid(user.pk),
                                                                     token=default_token_generator.make_token(user))
        return context


class RegisterComplete(BaseEmailMessage):
    template_name = "mail/EmailRegisterSuccess.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        return context
