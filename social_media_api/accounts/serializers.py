from rest_framework import serializers
from .models import CustomUser

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'profile_picture']

class CustomUserSerializer(serializers.ModelSerializer):
    followers = FollowerSerializer(many=True, read_only=True)
    following = FollowerSerializer(many=True, source='followers', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'bio', 'profile_picture', 'followers', 'following']
        read_only_fields = ['id', 'following']