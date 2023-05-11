from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def item_image_path(instance, filename):
    extension = filename.split('.')[-1]
    return '/'.join(['item', str(instance.owner), (str(instance.uuid) + '.' + extension)])


def normal_item_image_size(file):
    MAX_SIZE = 5 * 1024 * 1024
    if file.size > MAX_SIZE:
        raise ValidationError(
            _("File size can't be larger than 5mb"),
            params={"Error": 'Error'},)