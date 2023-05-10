from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def category_logo_path(instance, filename):
    return '/'.join(['category', str(instance.name), filename])


def normal_category_logo_size(file):
    MAX_SIZE = 2 * 1024 * 1024
    if file.size > MAX_SIZE:
        raise ValidationError(
            _("File size can't be larger than 2mb"),
            params={"Error": 'Error'},)