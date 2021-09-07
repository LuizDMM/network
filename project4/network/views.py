from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import functions
from .forms import newPostForm
from .models import User, Post, Like


def index(request):
    posts = functions.getAllUserPostsAndLikes()
    variables = {"newPostForm": newPostForm, "posts": posts}

    if request.method == "POST":
        # Get form data
        form = newPostForm(request.POST)
        print(form)

        # Create post if data is valid
        if form.is_valid():
            functions.createPostFormAuthor(form, request.user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request, "network/index.html", {"newPostForm": form, "posts": posts}
            )
    else:
        return render(request, "network/index.html", variables)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def profile(request, username):
    if request.method == "GET":
        user = functions.ProfileData().get(request.user.username)
        return render(
            request,
            "network/profile.html",
            {
                "profile": functions.ProfileData().get(username),
                "isFollowing": user.checkIfIsFollowing(username),
            },
        )
    elif request.method == "POST":  # Create a form in the view that the submit button follows.
        functions.followOrUnfollowFollowedFollowing(username, request.user.username)
        return HttpResponseRedirect(reverse("profile", args=[username]))


@login_required
def following(request):
    pass