
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("posts/", views.posts, name="posts"),
    path("edit_post/", views.edit_post, name="edit_post"),
    path("like_or_unlike/", views.like_or_unlike, name="like_or_unlike"),
    path("follow/", views.follow, name="follow"),
    path("following_user/", views.following_user, name="following_user"),
    path("profile/<int:creator_id>/", views.profile, name="profile")
]
