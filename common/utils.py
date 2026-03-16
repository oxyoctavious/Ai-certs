from rest_framework.exceptions import NotFound


def get_object_or_not_found(model_class, **filters):
    try:
        return model_class.objects.get(**filters)
    except model_class.DoesNotExist as exc:
        raise NotFound(f'{model_class._meta.verbose_name.title()} not found.') from exc


def parse_bool(value):
    if value is None:
        return None

    normalized = str(value).strip().lower()
    if normalized in {'1', 'true', 'yes'}:
        return True
    if normalized in {'0', 'false', 'no'}:
        return False
    return None
