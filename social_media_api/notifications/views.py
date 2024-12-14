from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from .models import Notification
from posts.models import Post, Comment
from django.contrib.auth import get_user_model
from .serializers import NotificationSerializer
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
User = get_user_model()

class CreateNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, action_type, target_id):
        user = request.user
        target = None
        verb = ''
        
        # Check for the action type and create a notification
        if action_type == 'follow':
            # Get the target user
            try:
                target = get_object_or_404(User, id=target_id)
                verb = 'started following you'
            except ObjectDoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        elif action_type == 'like':
            # Get the target post
            try:
                target = get_object_or_404(Post, id=target_id)
                verb = 'liked your post'
            except ObjectDoesNotExist:
                return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        elif action_type == 'comment':
            # Get the target comment
            try:
                target = get_object_or_404(Comment, id=target_id)
                verb = 'commented on your post'
            except ObjectDoesNotExist:
                return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
        
        else:
            return Response({"detail": "Invalid action type."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the notification
        try:
            notification = Notification.objects.create(
                recipient=target.author if isinstance(target, (Post, Comment)) else target,
                actor=user,
                verb=verb,
                target_content_type=ContentType.objects.get_for_model(target),
                target_object_id=target.id
            )
            return Response({"detail": "Notification created successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Fetch notifications for the user, showing unread ones first
        notifications = Notification.objects.filter(recipient=user).order_by('-read', '-timestamp')
        
        # Serialize notifications
        serializer = NotificationSerializer(notifications, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
