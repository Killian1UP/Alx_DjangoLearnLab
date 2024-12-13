from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from rest_framework import generics 
from rest_framework.generics import GenericAPIView
# for profile view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer, RegisterUserSerializer

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Retrieve the authenticated user's profile.
        If format is HTML, render the profile.html template.
        Otherwise, return a JSON response.
        """
        user = request.user
        serializer = CustomUserSerializer(user)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """Update the authenticated user's profile."""
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        # Get the user to follow
        user_to_follow = CustomUser.objects.filter(id=user_id).first()
        if not user_to_follow:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the user cannot follow themselves
        if user_to_follow == request.user:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        # Add the user to the following list
        request.user.following.add(user_to_follow)

        return Response({'detail': 'You are now following this user.'}, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        # Get the user to unfollow
        user_to_unfollow = CustomUser.objects.filter(id=user_id).first()
        if not user_to_unfollow:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the user cannot unfollow themselves
        if user_to_unfollow == request.user:
            return Response({'detail': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        # Remove the user from the following list
        request.user.following.remove(user_to_unfollow)

        return Response({'detail': 'You have unfollowed this user.'}, status=status.HTTP_200_OK)