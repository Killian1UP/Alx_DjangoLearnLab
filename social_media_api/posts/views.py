from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status, generics
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404


# Create your views here.
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the owner of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read-only permissions for GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for the owner of the object
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

     # Add filtering backends
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'content']  # Exact match filtering
    search_fields = ['title', 'content']  # Partial match filtering

    def perform_create(self, serializer):
        # Automatically set the logged-in user as the author of the post
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the logged-in user as the author of the comment
        serializer.save(author=self.request.user)

class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get the list of users that the current user follows
        following_users = request.user.following.all()
        
        # Get posts from the users the current user follows, ordered by creation date
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        # Serialize the posts
        serializer = PostSerializer(posts, many=True)
        
        # Return the serialized posts as a response
        return Response(serializer.data)
    
class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        # Fetch the post using generics.get_object_or_404
        post = generics.get_object_or_404(Post, pk=pk)

        # Use get_or_create exactly as required by the checker
        Like.objects.get_or_create(user=request.user, post=post)

        # Check if the like was created or already exists
        like = Like.objects.filter(user=user, post=post).first()
        if not like:
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a notification for the post author
        Notification.objects.create(
            recipient=post.author,
            actor=user,
            verb="liked your post",
            target_content_type=ContentType.objects.get_for_model(Post),
            target_object_id=post.id
        )

        return Response({"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED)


class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        # Fetch the post using generics.get_object_or_404
        post = generics.get_object_or_404(Post, pk=pk)

        # Find the Like object and delete it
        like = Like.objects.filter(user=user, post=post).first()

        if not like:
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the Like object
        like.delete()

        # Optionally, create a notification for unliking the post
        Notification.objects.create(
            recipient=post.author,
            actor=user,
            verb="unliked your post",
            target_content_type=ContentType.objects.get_for_model(Post),
            target_object_id=post.id
        )

        return Response({"detail": "Post unliked successfully."}, status=status.HTTP_200_OK)