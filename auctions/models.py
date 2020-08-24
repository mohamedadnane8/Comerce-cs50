from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # it inherits from the the AbstractUser (so it already have the username password and email!)
    pass


class Bid(models.Model):
    price = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(auto_now_add=True)
    # TO DO: Have to fix the default
    # I have to fix this default
    auction_listing = models.ForeignKey(
        "AuctionListing", on_delete=models.CASCADE, default="Bid(price=0)"
    )


class AuctionListing(models.Model):
    image = models.ImageField()
    details = models.TextField(max_length=400)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    comment = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    auction_listing = models.ForeignKey("AuctionListing", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=50)
    auction_listing = models.ManyToManyField(AuctionListing)
