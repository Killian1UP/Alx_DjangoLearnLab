from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField() 

    def __init__(self):
        return self.title

class CustomUserManager(BaseUserManager):
    def create_user(self, username, date_of_birth, profile_photo, password=None):
        if not username:
            raise ValueError("The username is required")
        if not date_of_birth:
            raise ValueError("The date of birth is required")
        
        user = self.model(username=username, date_of_birth=date_of_birth, profile_photo=profile_photo)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, date_of_birth=None, profile_photo=None, password=None):
        if not username:
            raise ValueError("The username is required")
        if date_of_birth is None:
            date_of_birth = '2000-01-01'  # Provide a default date if none is provided
        if profile_photo is None:
            profile_photo = 'default_profile_photo.jpg'
        
        
        user = self.create_user(username=username, password=password, date_of_birth=date_of_birth, profile_photo=profile_photo)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.username
    
class Post(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        permissions = [
            ("can_view", "Can view a post"),
            ("can_create", "Can create a post"),
            ("can_edit", "Can edit a post"),
            ("can_delete", "Can delete a post"),
        ]