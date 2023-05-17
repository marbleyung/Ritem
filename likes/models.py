from django.db import models
from account.models import CustomUser
from item.models import Item


class UserItemRelation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='my_likes')
    item = models.ForeignKey(Item, on_delete=models.CASCADE,
                             related_name='users_to_item')
    like = models.BooleanField(default=None)
