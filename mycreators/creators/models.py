from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Creator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='creator_avatars/', null=True, blank=True)
    about_me = models.TextField(blank=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)


    def __str__(self):
        return self.user.username

class Post(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.creator.user.username}'s post at {self.created_at}"