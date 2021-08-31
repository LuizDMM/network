from datetime import datetime
from django import forms

from .forms import newPostForm
from .models import User, Post, LikeRelations


def createPostFormAuthor(form, author):
    # Complement form data
    postData = form.save(commit=False)
    postData.author = User.objects.get(pk=author.id)
    postData.dateTime = datetime.now()
    print(postData)
    postData.save()
