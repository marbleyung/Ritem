from rest_framework import serializers
from .models import UserItemRelation


class UserItemRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserItemRelation
        fields = ('id', 'item', 'like')

