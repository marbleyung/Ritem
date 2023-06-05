from .models import Image, Item, UserItemRelation
from rest_framework import serializers
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


class UserItemRelationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    item = serializers.ReadOnlyField(source='item.name')

    class Meta:
        model = UserItemRelation
        fields = ('user', 'item',)

    def update(self, instance, validated_data):
        instance.like = validated_data['like']
        instance.save()
        return instance


class ItemGetSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)
    tags = TagSerializer(many=True, required=False)
    annotated_likes = serializers.IntegerField(read_only=True)
    annotated_dislikes = serializers.IntegerField(read_only=True)
    rating = serializers.SerializerMethodField()

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
                  'annotated_likes',
                  'annotated_dislikes',
                  'rating',
                  )

        extra_kwargs = {'owner': {'read_only': True},
                        'id': {'read_only': True},
                        'edited_at': {'read_only': True}}

        depth = 0

    def get_like(self, instance):
        relation = UserItemRelation.objects.get(
            item=instance, user=self.context['request'].user)
        return relation.like

    def get_rating(self, instance):
        if instance.annotated_dislikes == 0:
            if instance.annotated_likes == 0:
                return f"0%"
            return f"100%"
        percentage = int((instance.annotated_likes / (instance.annotated_likes + instance.annotated_dislikes)) * 100)
        return f"{percentage}%"
