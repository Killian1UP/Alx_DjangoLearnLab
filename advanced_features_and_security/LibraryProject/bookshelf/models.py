from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

def __init__(self):
    return self.name

class UserManager(BaseUserManager):
    def create_user(self, date_of_birth, profile_photo, password=None):
        if not date_of_birth:
            raise ValueError("The date of birth is required")
        user = self.model(date_of_birth=date_of_birth, profile_photo=profile_photo)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, date_of_birth, profile_photo, password=None):
        user = self.create_user(password=password, date_of_birth=date_of_birth, profile_photo=profile_photo)
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username