from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField

# Create your models here.

class Creator(models.Model):

    CREATOR_TYPES = [
        ('PHOTOGRAPHER', 'Photographer'),
        ('GAME_DEVELOPER', 'Game Developer'),
        ('CONTENT_CREATOR', 'Content Creator'),
        ('ARTIST', 'Artist'),
        ('VOICE_ACTOR', 'Voice Actor'),
        ('OTHER', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='creator_avatars/', null=True, blank=True)
    about_me = models.TextField(blank=True)
    creator_type = models.CharField(max_length=20, choices=CREATOR_TYPES, default='OTHER')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    request_message = models.TextField(blank=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_creator_type_display()} ({self.get_status_display()})"

class Post(models.Model):
    creator = models.ForeignKey('Creator', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200, default="Untitled Post")
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comments = models.JSONField(default=list)

    def add_comment(self, user, content):
        comment = {
            'id': len(self.comments) + 1, 
            'user_id': user.id,
            'username': user.username,
            'content': content,
            'created_at': timezone.now().isoformat()
        }
        self.comments.append(comment)
        self.save()

    def delete_comment(self, comment_id):
        self.comments = [c for c in self.comments if c['id'] != comment_id]
        self.save()

    def __str__(self):
        return f"{self.title} - by {self.creator.user.username} at {self.created_at}"