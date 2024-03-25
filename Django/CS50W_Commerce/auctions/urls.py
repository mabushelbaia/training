from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("wishlist/<int:listing_id>", views.wishlist, name="wishlist"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("closed", views.closed, name="closed"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
]
