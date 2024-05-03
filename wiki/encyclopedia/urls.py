from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("new page", views.new_page, name="new page"),
    path("edit entry/<str:title>", views.edit_entry, name="edit entry"),
    path("random", views.random_page, name="random")
]
