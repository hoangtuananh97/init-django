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
