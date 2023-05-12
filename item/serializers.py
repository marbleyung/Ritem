from django.db.models import Prefetch

from .models import Image, Item
from rest_framework import serializers
from category.models import Tag
from category.serializers import TagSerializer


class ImageSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    # item = serializers.ReadOnlyField()

    class Meta:
        model = Image
        fields = ('image', 'id')


class ItemCreateSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    image = serializers.ImageField(
        max_length=None,
        use_url=True,
        required=True
    )
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Item
        fields = ('category',
                  'id',
                  'tags',
                  'name',
                  'description',
                  'owner',
                  'image',
                  )


class ItemGetSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Item
        fields = ('category',
                  'tags',
                  'name',
                  'description',
                  'images',
                  'edited_at',
                  'owner',
                  'id',
                  )
        extra_kwargs = {'owner': {'read_only': True},
                        'id': {'read_only': True},
                        'edited_at': {'read_only': True}}

        depth = 0

