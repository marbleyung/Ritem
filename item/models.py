from django.db import models
from category.models import Category, Tag
from .models_services import *
from account.models import CustomUser
import uuid


class Image(models.Model):
    image = models.FileField(upload_to=item_image_path,
                             validators=[normal_item_image_size])
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4)
    extension = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.pk} {self.owner}"

    def save(self, *args, **kwargs):
        self.extension = str(self.image).split('.')[-1]
        super(Image, self).save(*args, **kwargs)


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='items')
    tags = models.ManyToManyField(Tag)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2_000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    image = models.ManyToManyField(Image)
    # reports = models.ManyToManyField(Report)

    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return f"{self.category}: {self.name}"


