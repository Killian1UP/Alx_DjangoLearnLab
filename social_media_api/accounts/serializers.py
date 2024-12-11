from rest_framework import serializers
from .models import CustomUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

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

class RegisterUserSerializer(serializers.ModelSerializer):
    # Explicitly defining password as a CharField with write-only access
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'bio', 'profile_picture']
    
    def create(self, validated_data):
       # Pop the password field before passing it to the create_user method
        password = validated_data.pop('password')
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(password)  # Set the password securely
        user.save()
        Token.objects.create(user=user)  # Create a token upon user creation
        return user