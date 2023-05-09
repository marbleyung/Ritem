from rest_framework import serializers
from .models import CustomUser, UserImage


class UserImageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = UserImage
        fields = ('image', 'owner')


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'password', 'first_name', 'last_name',
                  'username', 'phone', 'email', 'avatar',)
        extra_kwargs = {'password': {'write_only': True}}

