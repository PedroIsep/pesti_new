from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings

def get_default_author_id():
    return get_user_model().objects.get(username='default_username').id

class Image(models.Model):
    name = models.CharField(max_length=100)
    image = models.BinaryField()
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="images", 
        default=get_default_author_id
    )
        
    def __str__(self):
        return self

class Video(models.Model):
    name = models.CharField(max_length=100)
    video = models.FileField(upload_to='videos/')
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="videos"
    )
    
    def __str__(self):
        return self