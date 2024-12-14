from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.CharField(source='actor.username', read_only=True)  # Show the actor's username
    target = serializers.CharField(source='target.__str__', read_only=True)  # Show the target's string representation
    target_type = serializers.CharField(source='target_content_type.model', read_only=True)  # Target's content type (model name)
    
    class Meta:
        model = Notification
        fields = ['actor', 'verb', 'timestamp', 'read', 'target', 'target_type']
