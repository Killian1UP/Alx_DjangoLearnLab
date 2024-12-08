from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Post, Comment
from taggit.forms import TagWidget

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']

# Created Post Form to handle the creation and updating of blog posts
class PostForm(forms.ModelForm):
    class Meta:
        model = Post 
        fields = ['title', 'content', 'tags']  # added tags
        widgets = {
            'tags': TagWidget(),  # Use TagWidget for the tags field
        }

# Utilized widgets to provide a larger input area, suitable for comments.
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your comment here...',
                'rows': 4,
                'cols': 50,
            })
        }
        labels = {
            'content': 'Comment'
        }