from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
User = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actions')
    verb = models.CharField(max_length=255)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # The type of the target object
    object_id = models.PositiveIntegerField()  # The ID of the target object
    
    # The actual target object is a GenericForeignKey
    target = GenericForeignKey('content_type', 'object_id')
    
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # Tracks if the notification has been read

    def __str__(self):
        return f"{self.actor} {self.verb} {self.target} for {self.recipient}"