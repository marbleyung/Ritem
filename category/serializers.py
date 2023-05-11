from rest_framework import serializers
from .models import Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'logo', 'parent', 'id', 'slug')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    def to_internal_value(self, data):
        name = data.get('name')
        tag, created = Tag.objects.get_or_create(name=name)
        return {'tag': tag}
