from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # it inherits from the the AbstractUser (so it already have the username password and email!)
    # watchlist = models.ForeignKey("AuctionListing",on_delete= models.CASCADE)

    def __str__(self):
        return self.username


class Bid(models.Model):
    price = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    auction_listing = models.ForeignKey("AuctionListing", on_delete=models.CASCADE)

    # TO DO: Have to fix the default
    # I have to fix this default

    def __str__(self):
        return self.price


class AuctionListing(models.Model):
    title = models.CharField(max_length=60)
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        default=None,
        related_name="auctionlisting",
    )
    image = models.URLField()
    details = models.TextField(max_length=400)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    date = models.DateTimeField(auto_now_add=True)

    # TODO: I shoud set this to default

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auction_listing = models.ForeignKey(
        "AuctionListing", on_delete=models.CASCADE, default=None
    )
    date = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # TODO have to think about related name
    def __str__(self):
        return self.name
