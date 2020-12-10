from django.contrib.auth.tokens import default_token_generator
from djoser.email import ActivationEmail

from app.utils import utils


class CustomActionEmail(ActivationEmail):
    template_name = "mail/EmailActivation.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["url"] = 'auth/users/activate/{uid}/{token}'.format(uid=utils.encode_uid(user.pk),
                                                                    token=default_token_generator.make_token(user))
        return context
