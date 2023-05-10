from rest_framework import serializers
from .models import Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'logo', 'parent', 'id', 'slug')
