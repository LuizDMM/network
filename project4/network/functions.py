from datetime import datetime
from django import forms

from .forms import newPostForm
from .models import User, Post, Like, FollowRelations


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
    for item in postsQueried:
        data = PostData()
        data.author = item.author
        data.dateTime = item.dateTime
        data.content = item.content
        data.likes = Like.objects.filter(post=item).count()
        postsToReturn.append(data)
    return postsToReturn


class ProfileData():
    def __init__(self):
        self.username = "Username"
        self.following = 0
        self.followers = 0
        self.posts = []


def getProfileData(username):
    userModelData = User.objects.get(username=username)
    postModelData = Post.objects.filter(author=userModelData).order_by("-dateTime")
    profileData = ProfileData()
    profileData.username = username
    profileData.following = FollowRelations.objects.filter(following=userModelData).count()
    profileData.followers = FollowRelations.objects.filter(followed=userModelData).count()
    for post in postModelData:
        profileData.posts.append(post)
    return profileData
    