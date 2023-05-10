import mptt.admin
from django.contrib import admin
from .models import Category, Tag


class CategoryAdmin(mptt.admin.MPTTModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
