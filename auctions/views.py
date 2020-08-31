from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import *


def index(request):
    return render(
        request, "auctions/index.html", {"products": AuctionListing.objects.all()}
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        start_bid = float(request.POST["start_bid"])
        if start_bid < 0:
            return render(
                request,
                "auctions/createListing.html",
                {
                    "categories": categories,
                    "message": "Starting Bid Should be positive!",
                },
            )
        try:
            category = Category.objects.get(pk=int(request.POST["category"]))
        except:
            return render(
                request,
                "auctions/createListing.html",
                {"categories": categories, "message": "You should precise a category!"},
            )

        image = request.POST["image_URL"]

        product = AuctionListing.objects.create(
            title=title,
            category_id=int(request.POST["category"]),
            image=image,
            description=description,
            user=request.user,
        )
        initial_bid = Bid.objects.create(bid_value=start_bid, product=product)

        return HttpResponseRedirect(reverse("index"))
    else:
        categories = Category.objects.all()
        return render(
            request, "auctions/createListing.html", {"categories": categories}
        )


def listing(request, product_id):
    product = AuctionListing.objects.get(pk=product_id)
    if product:
        return render(request, "auctions/listing.html", {"product": product})
    else:
        # return error
        pass


@login_required
def bid(request, id):
    print("Hello world /n\n\n\n\n")

    if request.method == "POST":
        product = AuctionListing.objects.get(pk=id)

        try:
            bid_value = float(request.POST["bid-value"])
        except ValueError:
            message = "Please imput something before submiting the bid"

        if bid_value > product.bid_product.last().bid_value:
            message = "Your bid was accepted"

            Bid.objects.create(bid_value=bid_value, product=product)
        else:
            message = "Your bid should be higher than the current bid"

        return redirect("listing", product_id=id)

    else:
        return redirect("index")
