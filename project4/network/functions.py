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


def getFollowingPostsAndLikes(usernames):
    postsToReturn = []

    for item in usernames:
        profile = ProfileData().get(item)
        for post in profile.posts:
            postsToReturn.append(post)

    return postsToReturn

    
class ProfileData:
    def __init__(self):
        self.username = "Username"
        self.following = 0
        self.followers = 0
        self.posts = []

    def checkIfIsFollowing(self, username):
        selfDataQuery = User.objects.get(username=self.username)
        userToCheckDataQuery = User.objects.get(username=username)
        followRelationQuery = FollowRelations.objects.filter(
            following=selfDataQuery
        ).filter(followed=userToCheckDataQuery)
        if followRelationQuery.count() > 0:
            return True
        return False

    def get(self, username):
        userModelData = User.objects.get(username=username)
        postModelData = Post.objects.filter(author=userModelData).order_by("-dateTime")
        self.username = username
        self.following = FollowRelations.objects.filter(
            following=userModelData
        ).count()
        self.followers = FollowRelations.objects.filter(
            followed=userModelData
        ).count()
        for post in postModelData:
            self.posts.append(post)
        return self


def followOrUnfollowFollowedFollowing(followed, following):
    followingData = ProfileData().get(following)
    followedData = ProfileData().get(followed)
    if followingData.checkIfIsFollowing(followedData.username) == False:
        FollowRelations(followed=User.objects.get(username=followedData.username), following=User.objects.get(username=followingData.username)).save()
        return True
    FollowRelations.objects.filter(followed=User.objects.get(username=followedData.username), following=User.objects.get(username=followingData.username)).delete()
    return True