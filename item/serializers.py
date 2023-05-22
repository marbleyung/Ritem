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
    relation = serializers.SerializerMethodField()

    class Meta:
        model = UserItemRelation
        fields = ('user', 'item', 'relation')

    def update(self, instance, validated_data):
        relation, _ = UserItemRelation.objects.get_or_create(
            item=instance, user=self.context['request'].user)
        relation.like = validated_data['like']
        relation.save()
        return instance

    def get_relation(self, instance):
        relation = UserItemRelation.objects.get(
            item=instance, user=self.context['request'].user)
        return {"like": relation.like,
                'item': instance.name,
                'user': self.context['request'].user.username}


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
