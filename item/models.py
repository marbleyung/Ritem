from django.db import models
from category.models import Category, Tag
from .models_services import *
from account.models import CustomUser
import uuid


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='items')
    tags = models.ManyToManyField(Tag, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2_000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                              default=1, related_name='my_items')
    users = models.ManyToManyField(CustomUser, through='UserItemRelation',
                                   related_name='rated_items')

    # reports = models.ManyToManyField(Report)

    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return f"{self.category}: {self.name}"

    @property
    def images(self):
        return self.image_set.all()

    @property
    def count_images(self):
        return self.images.count


class UserItemRelation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='my_likes')
    item = models.ForeignKey(Item, on_delete=models.CASCADE,
                             related_name='users_to_item')
    like = models.BooleanField(null=True)

    class Meta:
        unique_together = ('user', 'item')

    def __str__(self):
        if self.like is False:
            return f"{self.user} dislikes {self.item}"
        elif self.like:
            return f"{self.user} likes {self.item}"
        return f"{self.user} haven't rated {self.item} yet"


class Image(models.Model):
    image = models.FileField(upload_to=item_image_path,
                             validators=[normal_item_image_size])
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                              related_name='my_images')
    uuid = models.UUIDField(default=uuid.uuid4)
    extension = models.CharField(max_length=10, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.pk} {self.owner}"

    def save(self, *args, **kwargs):
        self.extension = str(self.image).split('.')[-1]
        super(Image, self).save(*args, **kwargs)

