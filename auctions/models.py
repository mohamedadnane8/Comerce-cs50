from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    # it inherits from the the AbstractUser (so it already have the username password and email!)
    pass
class Bid(models.Model):
    price = models.FloatField()
    user = models.ForeignKey(User,on_delete= models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)
    
class AuctionListing(models.Model):
    image = models.ImageField()
    details = models.TextField(max_length=400)
    title  = models.CharField(max_length=60)
    date = models.DateTimeField(auto_now_add=True)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE)

class Comment(models.Model):
    comment  = models.CharField(max_length=200)
    user = models.ForeignKey(User,on_delete= models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)
    