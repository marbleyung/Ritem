from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    phone = PhoneNumberField(null=True, blank=False)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='media/user/avatar/')
    bio = models.CharField(max_length=255, blank=True, null=True)
    is_online = models.BooleanField(default=True)

    REQUIRED_FIELDS = ('email', 'phone',)

    class Meta:
        verbose_name = 'Custom User'

