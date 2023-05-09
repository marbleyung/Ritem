from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


def avatar_path(instance, filename):
    return '/'.join(['user_image', str(instance.owner), filename])


class UserImage(models.Model):
    owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=avatar_path, blank=True)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    phone = PhoneNumberField(null=True, blank=False, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.ForeignKey(UserImage, null=True, on_delete=models.SET_NULL)
    bio = models.CharField(max_length=255, blank=True, null=True)
    is_online = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email', 'phone',)

    class Meta:
        verbose_name = 'Custom User'

