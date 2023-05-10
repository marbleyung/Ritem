from django.db import models
from django.utils.text import slugify
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from .models_services import *


class Category(MPTTModel):
    name = models.CharField(max_length=30)
    logo = models.FileField(upload_to=category_logo_path, blank=True,
                            validators=[normal_category_logo_size])
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    parent = TreeForeignKey('self', related_name='children',
                            on_delete=models.SET_NULL,
                            null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        unique_together = ('slug', 'parent')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.parent:
            self.slug = f'{self.parent.slug}-{slugify(self.name)}'
        else:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)
