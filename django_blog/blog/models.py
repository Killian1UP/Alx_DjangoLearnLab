from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    tags = TaggableManager()

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tag(models.Model):
    name = models.CharField(max_length=100)
    post = models.ManyToManyField(Post, related_name='posts')

class TaggedPost(GenericTaggedItemBase):
    tag = models.ForeignKey('MyCustomTag', on_delete=models.CASCADE, related_name="tagged_items")

class MyCustomTag(TagBase):
    slug = models.SlugField(unique=True, max_length=100)