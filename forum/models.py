# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    title = models.CharField(max_length=255)
    content = models.TextField()
    users_liked = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    no_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Reply(models.Model):
    content = models.TextField()
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='replies',default=None)
    

    def __str__(self):
        return f'Reply to {self.post.title}'






