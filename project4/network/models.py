from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="author")
    content = models.TextField()
    dateTime = models.DateTimeField()


class Like(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    personThatLike = models.ForeignKey("User", on_delete=models.CASCADE)


class FollowRelations(models.Model):
    followed = models.ForeignKey("User", on_delete=models.CASCADE, related_name='followed',)
    following = models.ForeignKey("User", on_delete=models.CASCADE, related_name='following')