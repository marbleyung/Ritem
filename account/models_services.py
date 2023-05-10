import os

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def avatar_path(instance, filename):
    return '/'.join(['user_image', str(instance.owner), filename])


def normal_filesize(file):
    MAX_SIZE = 2 * 1024 * 1024
    if file.size > MAX_SIZE:
        raise ValidationError(
            _("File size can't be larger than 2mb"),
            params={"Error": 'Error'},)