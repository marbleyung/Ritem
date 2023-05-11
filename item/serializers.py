from .models import Image, Item
from rest_framework import serializers
from category.models import Tag


class ImageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    item = serializers.ReadOnlyField()

    class Meta:
        model = Image
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='slug',
        required=False
    )
    image = serializers.ImageField(
        max_length=None,
        use_url=True,
        required=True
    )

    class Meta:
        model = Item
        fields = ('category',
                  'tags',
                  'name',
                  'description',
                  'edited_at',
                  'image',
                  )

