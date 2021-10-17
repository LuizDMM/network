import json
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from . import functions
from .forms import newPostForm, editPostForm
from .models import User, Post, Like, FollowRelations


def index(request):
    # Variable declaration and pagination logic
    posts = functions.getAllUserPostsAndLikes()
    for item in posts:
        user = User.objects.get(id=request.user.id)
        post = Post.objects.get(id=item.id)
        item.liked = functions.checkIfUserLikedPost(user, post)
    postsPaginator = Paginator(posts, 10)
    page_num = request.GET.get("page")
    page = postsPaginator.get_page(page_num)
    variables = {"newPostForm": newPostForm, "page": page, "user": request.user}

    if request.method == "POST":
        # Get form data
        form = newPostForm(request.POST)
        print(form)

        # Create post if data is valid
        if form.is_valid():
            functions.createPost(form, request.user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "network/index.html",
                {"newPostForm": form, "page": page, "user": request.user.username},
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
        currentUser = functions.ProfileData().get(request.user.username)
        postsPaginator = Paginator(functions.ProfileData().get(username).posts, 10)
        page_num = request.GET.get("page")
        page = postsPaginator.get_page(page_num)

        return render(
            request,
            "network/profile.html",
            {
                "profile": functions.ProfileData().get(username),
                "isFollowing": currentUser.checkIfIsFollowing(username),
                "page": page,
            },
        )
    elif (
        request.method == "POST"
    ):  # Create a form in the view that the submit button follows.
        functions.followOrUnfollowFollowedFollowing(username, request.user.username)
        return HttpResponseRedirect(reverse("profile", args=[username]))


@login_required
def following(request):
    # Get the follow relations
    profilesThatUserFollows = FollowRelations.objects.filter(
        following=User.objects.get(username=request.user.username)
    )

    # Create a list with the usernames of all the users that the user is following
    usernames = []
    for profile in profilesThatUserFollows:
        usernames.append(profile.followed.username)

    # Get the posts from all the users that the user is following
    posts = functions.getFollowingPostsAndLikes(usernames)

    # Add the like information 
    for item in posts:
        user = User.objects.get(id=request.user.id)
        post = Post.objects.get(id=item.id)
        item.liked = functions.checkIfUserLikedPost(user, post)

    # Paginate the posts
    postsPaginator = Paginator(posts, 10)
    page_num = request.GET.get("page")
    page = postsPaginator.get_page(page_num)

    return render(
        request,
        "network/following.html",
        {"page": page},
    )


@login_required
@csrf_exempt
def post(request, id):
    if request.method == "PUT":
        user = User.objects.get(id=request.user.id)
        post = Post.objects.get(id=id)
        userLikedPost = functions.checkIfUserLikedPost(user, post)
        print(userLikedPost)
        if userLikedPost:
            Like.objects.filter(post=post, personThatLike=user).delete()
            render(
                request,
                "network/postDiv.html",
                {
                    "post": functions.getPost(id),
                    "liked": functions.checkIfUserLikedPost(user, post),
                },
            )
        else:
            like = Like(post=post, personThatLike=user)
            like.save()
            return render(
                request,
                "network/postDiv.html",
                {
                    "post": functions.getPost(id),
                    "liked": functions.checkIfUserLikedPost(user, post),
                },
            )

    return render(
        request,
        "network/postDiv.html",
        {
            "post": functions.getPost(id),
            "liked": functions.checkIfUserLikedPost(user, post),
        },
    )


@login_required
def edit_post(request, id):
    # Query the post
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "The post does not exist."}, status=400)

    # Check if the user is the post's author.
    if request.user.id != post.author.id:
        return JsonResponse({"error": "You can't edit this post."}, status=400)

    # If request method is POST, modify the post
    if request.method == "POST":
        form = editPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return render(
                request,
                "network/postDiv.html",
                {"post": functions.getPost(id)},
                status=201,
            )

    # If request method is GET: return the form
    form = editPostForm(instance=post)
    return render(request, "network/editPostForm.html", {"form": form, "id": id})
