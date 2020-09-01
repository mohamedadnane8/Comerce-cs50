from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # it inherits from the the AbstractUser (so it already have the username password and email!)
    def __str__(self):
        return self.username


class Bid(models.Model):
    bid_value = models.FloatField(default=0)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="bid_owner"
    )
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        "AuctionListing", on_delete=models.CASCADE, related_name="bid_product"
    )

    # TO DO: Have to fix the default
    # I have to fix this default

    def __str__(self):
        return f"{self.bid_value}"


class AuctionListing(models.Model):
    title = models.CharField(max_length=60)
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        related_name="auction_category",
    )
    image = models.URLField()
    description = models.TextField(max_length=400)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="auction_owner"
    )
    winner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="auction_winner"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_sold = models.DateTimeField(auto_now=False, blank=True, null=True)

    # TODO: I shoud set this to default
    def is_active(self):
        return self.winner == None

    def current_price(self):
        return self.bid_product.last().bid_value

    def __str__(self):
        return self.title


class Watchlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_watching"
    )
    products = models.ForeignKey(
        AuctionListing,
        on_delete=models.SET_NULL,
        null=True,
        related_name="watched_item",
    )

    def __str__(self):
        return f"{self.products.id}: {self.user.username}"


class Comment(models.Model):
    comment = models.CharField(max_length=200)
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, related_name="comment_owner", null=True
    )
    auction_listing = models.ForeignKey(
        "AuctionListing",
        on_delete=models.CASCADE,
        default=None,
        related_name="auction_commented",
    )
    date = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # TODO have to think about related name
    def __str__(self):
        return self.name
