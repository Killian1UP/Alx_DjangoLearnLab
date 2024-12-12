from rest_framework import serializers
from .models import Post, Comment 
from django.contrib.auth import get_user_model

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username') # Display the author's username

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_title(self, value):
        """Ensure the title is not empty."""
        if not value.strip():
            raise serializers.ValidationError("Title cannot be blank.")
        return value

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')  # Display the author's username
    post_title = serializers.ReadOnlyField(source='post.title')  # Display the post title

    class Meta:
        model = Comment
        fields = ['id', 'post', 'post_title', 'author', 'author_username', 'content', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_content(self, value):
        """Ensure the content is not empty."""
        if not value.strip():
            raise serializers.ValidationError("Comment content cannot be blank.")
        return value