from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


class User(AbstractUser):
    pass

class Followers(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followed', on_delete=models.CASCADE)


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)
    date = models.DateTimeField(default=timezone.now)
    
    def likes_count(self):
        return self.likes.count()
    
    def user_liked_post(self, user):
        return self.likes.filter(user=user).exists()

class Likes(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="liked")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes")