
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("u/<str:username>",views.profile, name="profile"),
    path("post/post-<int:id>",views.post, name="postDiv"),
    path("post/post-<int:id>/edit", views.edit_post, name="editPost"), 
]
