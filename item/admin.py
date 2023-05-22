from django.contrib import admin
from .models import Image, Item, UserItemRelation


class ImageInline(admin.TabularInline):
    model = Image


class ItemAdmin(admin.ModelAdmin):
    inlines = [ImageInline]

    class Meta:
        model = Item
        fields = ('category', 'name', 'tags', 'id',
                  'description', 'created_at',
                  'edited_at', 'is_published',)


admin.site.register(Image)
admin.site.register(Item, ItemAdmin)
admin.site.register(UserItemRelation)