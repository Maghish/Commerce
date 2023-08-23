from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("category", views.all_category_view, name="all_category_view"),
    path("category/<str:category_name>", views.category_view, name="category_view"),
    path("listing/<int:listing_id>", views.listing_view, name="listing_view"),
    path("watchlist/remove/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("watchlist/add/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("watchlist", views.watchlist_view, name="watchlist_view"),
    path("edit/<int:listing_id>", views.edit_listing, name="edit_listing"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("closed", views.closed_view, name="closed_view"),
    path("closed/<int:listing_id>", views.close_listing, name="close_listing")
]
