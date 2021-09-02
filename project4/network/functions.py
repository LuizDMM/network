from datetime import datetime
from django import forms

from .forms import newPostForm
from .models import User, Post, Like


def createPostFormAuthor(form, author):
    # Complement form data
    postData = form.save(commit=False)
    postData.author = User.objects.get(pk=author.id)
    postData.dateTime = datetime.now()
    postData.save()


class PostData:
    def __init__(self):
        self.author = "author"
        self.dateTime = "datetime"
        self.content = "content"
        self.likes = 0


def getAllUserPostsAndLikes():
    postsQueried = Post.objects.all().order_by("-dateTime")
    postsToReturn = []
    data = PostData()
    for item in postsQueried:
        data.author = item.author
        data.dateTime = item.dateTime
        data.content = item.content
        data.likes = Like.objects.filter(post=item).count()
        postsToReturn.append(data)
    return postsToReturn