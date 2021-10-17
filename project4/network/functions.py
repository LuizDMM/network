from datetime import datetime
from django import forms

from .forms import newPostForm
from .models import User, Post, Like, FollowRelations


def createPost(form, author):
    # Complement form data
    postData = form.save(commit=False)
    postData.author = User.objects.get(pk=author.id)
    postData.dateTime = datetime.now()
    postData.save()


class PostData:
    def __init__(self):
        self.id = 0
        self.author = "author"
        self.dateTime = "datetime"
        self.content = "content"
        self.likes = 0

    def get(self, id):
        postData = Post.objects.get(id=id)
        self.id = id
        self.author = postData.author
        self.dateTime = postData.dateTime
        self.content = postData.content
        self.likes = Like.objects.filter(post=postData).count()
        return self


def getAllUserPostsAndLikes():
    postsQueried = Post.objects.all().order_by("-dateTime")
    postsToReturn = []
    for item in postsQueried:
        data = PostData()
        data.id = item.id
        data.author = item.author
        data.dateTime = item.dateTime
        data.content = item.content
        data.likes = Like.objects.filter(post=item).count()
        postsToReturn.append(data)
    return postsToReturn


def getPost(id):
    postQueried = Post.objects.get(id=id)
    postToReturn = PostData()
    postToReturn.id = postQueried.id
    postToReturn.author = postQueried.author
    postToReturn.dateTime = postQueried.dateTime
    postToReturn.content = postQueried.content
    postToReturn.likes = Like.objects.filter(post=postQueried).count()
    return postToReturn


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


def checkIfUserLikedPost(user, post):
    if Like.objects.filter(post=post, personThatLike=user).count() > 0:
        return True
    else:
        return False