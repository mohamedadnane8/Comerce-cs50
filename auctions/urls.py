from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_listing, name="createListing"),
    path("bid/<int:id>/", views.bid, name="bid"),
    path("<int:product_id>/", views.listing, name="listing"),
    path("close/<int:id>/", views.close, name="close"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist-add/<int:product_id>/", views.add_watchlist, name="addWatchlist"),
    path(
        "watchlist-del/<int:product_id>/",
        views.delete_watchlist,
        name="deleteWatchlist",
    ),
]
