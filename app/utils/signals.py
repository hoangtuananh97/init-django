from django.dispatch import Signal

user_registered = Signal(providing_args=['user', 'request'])

user_registered_complete = Signal(providing_args=['user', 'request'])
