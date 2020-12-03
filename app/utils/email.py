from djoser.email import ActivationEmail


class CustomActionEmail(ActivationEmail):
    template_name = "mail/EmailActivation.html"
