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
