from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
    
from django.contrib.auth.models import User  # Import User model

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship with User
    name = models.CharField(max_length=255, blank=True)  # Customer name (optional)
    customer_id = models.CharField(max_length=20, unique=True, blank=True)  # Customer ID (optional, unique)
    email = models.EmailField(blank=True)  # Customer email (optional)
    cust_acc_num = models.CharField(max_length=20, unique=True, blank=True)  # Customer account number (optional, unique)
    rec_acc_num = models.CharField(max_length=20, unique=True, blank=True)  # Recipient account number (optional, unique)
    account_type = models.CharField(max_length=50, blank=True)  # Account type (optional)
    cust_old_bal = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)  # Customer old balance (optional)
    cust_new_bal = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)  # Customer new balance (optional)
    rec_old_bal = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)  # Recipient old balance (optional)
    rec_new_bal = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)  # Recipient new balance (optional)
    bio = models.TextField(blank=True)  # Customer bio (optional)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')  # Profile image (optional)
    location = models.CharField(max_length=100, blank=True)  # Customer location (optional)

    def __str__(self):
        return f"{self.user.username}'s Customer Profile"  # Improved string representation


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user