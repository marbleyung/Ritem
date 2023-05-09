from django.db.models import QuerySet
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserImage, CustomUser


@receiver(post_save, sender=UserImage)
def my_handler(sender, **kwargs):
    avatar = kwargs['instance']
    user = CustomUser.objects.filter(username=avatar.owner.username)
    user.update(avatar=avatar)
    print('line8', avatar)
    print('line9', user)
