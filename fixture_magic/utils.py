from django.db import models
import django.apps

serialize_me = []
seen = {}
at_top_position = 0


def reorder_json(data, models, ordering_cond=None):
    """Reorders JSON (actually a list of model dicts).

    This is useful if you need fixtures for one model to be loaded before
    another.

    :param data: the input JSON to sort
    :param models: the desired order for each model type
    :param ordering_cond: a key to sort within a model
    :return: the ordered JSON
    """
    if ordering_cond is None:
        ordering_cond = {}
    output = []
    bucket = {}
    others = []

    for model in models:
        bucket[model] = []

    for object in data:
        if object['model'] in bucket.keys():
            bucket[object['model']].append(object)
        else:
            others.append(object)
    for model in models:
        if model in ordering_cond:
            bucket[model].sort(key=ordering_cond[model])
        output.extend(bucket[model])

    output.extend(others)
    return output


def get_fields(obj, *exclude_fields):
    try:
        return [f for f in obj._meta.fields if f.name not in exclude_fields]
    except AttributeError:
        return []


def get_m2m(obj, *exclude_fields):
    try:
        return [f for f in obj._meta.many_to_many if f.name not in exclude_fields]
    except AttributeError:
        return []


def serialize_fully(exclude_fields):
    index = 0
    exclude_fields = exclude_fields or ()

    while index < len(serialize_me):
        # Serializing Foreign keys
        for field in get_fields(serialize_me[index], *exclude_fields):
            if isinstance(field, models.ForeignKey):
                add_to_serialize_list(
                    [serialize_me[index].__getattribute__(field.name)])

        # Serializing ManyToMany fields targets
        for field in get_m2m(serialize_me[index], *exclude_fields):
            field_manager = serialize_me[index].__getattribute__(field.name)

            add_to_serialize_list(field_manager.all())

        index += 1

    serialize_me.reverse()

    index = 0

    # Now we need to record all custom M2M models
    while index < len(serialize_me):
        # Serializing custom ManyToMany models, they should be last of all,
        # and as we will reverse serialized data we do it first.
        # Add through model to serialization, to allow correct parsing of fields
        # with related_name="+" in custom through models
        for field in get_m2m(serialize_me[index], *exclude_fields):
            field_manager = serialize_me[index].__getattribute__(field.name)
            custom_models = django.apps.apps.get_models()
            through_model = field_manager.through

            # Skip serialization of auto-created ManyToMany models, to exclude problems
            # on load data.
            if through_model not in custom_models:
                continue

            source_field_name = field_manager.source_field_name
            related_objects_ids = list(field_manager.related_val)
            through_filter = {f"{source_field_name}__in": related_objects_ids}

            through_objects = through_model.objects.filter(**through_filter).all()

            add_to_serialize_list(through_objects)

        index += 1

def add_to_serialize_list(objs, at_top=False):
    global at_top_position

    for obj in objs:
        if obj is None:
            continue
        if not hasattr(obj, '_meta'):
            add_to_serialize_list(obj)
            continue

        meta = obj._meta.proxy_for_model._meta if obj._meta.proxy else obj._meta
        model_name = getattr(meta, 'model_name',
                             getattr(meta, 'module_name', None))
        key = "%s:%s:%s" % (obj._meta.app_label, model_name, obj.pk)

        if key not in seen:
            if at_top:
                serialize_me.insert(at_top_position, obj)
                at_top_position += 1
            else:
                serialize_me.append(obj)
            seen[key] = 1
