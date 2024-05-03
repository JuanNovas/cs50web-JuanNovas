from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new listing", views.new_listing, name="new listing"),
    path("listing/<str:item>", views.listing_page, name="listing page"),
    path("bid/<str:item>", views.make_bid, name="make bid"),
    path("delete/<str:item>", views.delete_auction, name="delete auction"),
    path("new_comment/<str:item>", views.new_comment, name="new comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category/<str:category>", views.categorys, name="categorys"),
    path("category", views.categorys, name="categorys_no_category")
]
