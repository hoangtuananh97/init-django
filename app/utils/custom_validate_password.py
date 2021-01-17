from django.core.exceptions import ValidationError


class CustomValidatePassword:
    # min length password
    def __init__(self, min_length=8):
        self.min_length = min_length
        self.msg = 0

    # pass must have digit, alpha, special character
    def validate(self, password, user=None):

        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]+=_-"

        if not any(i.isdigit() for i in password):
            self.msg = 1
            raise ValidationError(
                'Password must contain at least character is digit.')
        if not any(i.isalpha() for i in password):
            self.msg = 2
            raise ValidationError(
                'Password must contain at least character is text.')
        if not any(i in special_characters for i in password):
            self.msg = 3
            raise ValidationError(
                'Password must contain at least character is special characters.')

    def get_help_text(self):
        return msg_validate_password(self.msg)


def msg_validate_password(msg_digit):
    msg = {
        1: 'Password must contain at least character is digit.',
        2: 'Password must contain at least character is text.',
        3: 'Password must contain at least character is special characters.',
        0: ''
    }
    return msg[msg_digit]
