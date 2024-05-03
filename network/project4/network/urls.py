
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("compose", views.new_post, name="new mail"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("profile/follow/<str:prof_username>", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("like/", views.like, name="like"),
    path("like-button/", views.like_button, name="like button")
]
