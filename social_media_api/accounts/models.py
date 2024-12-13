from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, bio, profile_picture, password, **extra_fields):
        if not username:
            raise ValueError("The username is required.")
        
        user = self.model(username=username, bio=bio, profile_picture=profile_picture, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, bio, profile_picture, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, bio, profile_picture, password, **extra_fields)

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_photos', blank=True, null=True, default='default_profile_picture.jpg')
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following_set')
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers_set')

    objects = CustomUserManager()

    def __str__(self):
        return self.username