from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE)
    content = models.TextField()
    dateTime = models.DateTimeField()

class Like(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    personThatLike = models.ForeignKey("User", on_delete=models.CASCADE)