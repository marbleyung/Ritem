from rest_framework import serializers
from .models import CustomUser, UserImage


class UserImageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = UserImage
        fields = ('image', 'owner', 'id',)


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name',
                  'username', 'phone', 'email', 'avatar',
                  'is_online',)


class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
