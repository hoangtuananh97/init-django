import base64

from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def field_representation(instance, fields):
    data = {}
    for field in fields:
        field_model = getattr(instance, field)
        if field_model:
            data.update({field: field_model.__repr__()})
    return data


def many_related_field_representation(instance, fields):
    data = {}
    for field in fields:
        models = getattr(instance, field).all()
        model_data = []
        if models.count() > 0:
            for model in models:
                model_data.append(model.__repr__())
            data.update({field: model_data})
    return data


def encode_uid(pk):
    return force_text(urlsafe_base64_encode(force_bytes(pk)))


def decode_uid(pk):
    return force_text(urlsafe_base64_decode(pk))


def decode_authorization(request):
    try:
        basic_auth = request.META['HTTP_AUTHORIZATION']
        basic_token = basic_auth.split(' ')[1]
        basic_token_encode = base64.b64decode(basic_token).decode()
        user_name = basic_token_encode.split(':')[0]
        password = basic_token_encode.split(':')[1]
        return user_name, password
    except Exception as e:
        return None, None
