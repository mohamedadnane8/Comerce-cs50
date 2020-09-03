from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import datetime

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
    is_watchlist = bool(
        product.watched_item and product.watched_item.all().filter(user=request.user)
    )
    if product:
        if request.user.id == product.user.id:
            return render(
                request,
                "auctions/listing.html",
                {"product": product, "ïs_owner": True},
            )

        return render(
            request,
            "auctions/listing.html",
            {"product": product, "is_watchlist": is_watchlist},
        )
    else:
        pass


# TODO: If the bid doesn’t meet those criteria, the user should be presented with an error.
@login_required(login_url="/login/")
def bid(request, id):

    if request.method == "POST":

        product = AuctionListing.objects.get(pk=id)

        try:
            bid_value = float(request.POST["bid-value"])
        except ValueError:
            message = "Please imput something before submiting the bid"

        if bid_value > product.current_price():
            message = "Your bid was accepted"

            Bid.objects.create(bid_value=bid_value, product=product, user=request.user)
        else:
            message = "Your bid should be higher than the current bid"

        return redirect("listing", product_id=id)

    else:
        return redirect("index")


@login_required
def close(request, id):
    product = AuctionListing.objects.get(pk=id)
    # these extra conditions can be deleted but just to make sure this is secure I added it
    if request.method == "POST" and product and request.user.id == product.user.id:
        winner_user = product.bid_product.last().user
        if winner_user == None:
            # TODO: I have to display an error (There is no bid)
            pass
        product.date_sold = datetime.datetime.now()
        product.winner = winner_user

        product.save()

        return redirect("index")
    return redirect("listing", product_id=id)


@login_required(login_url="/login/")
def watchlist(request):
    list_product = [p.products for p in request.user.user_watching.all()]
    return render(request, "auctions/watchlist.html", {"products": list_product},)


@login_required
def add_watchlist(request, product_id):
    if request.method == "POST":
        product = AuctionListing.objects.get(pk=product_id)
        Watchlist.objects.create(user=request.user, products=product)
        return redirect("listing", product_id=product_id)
    return redirect("index")


@login_required
def delete_watchlist(request, product_id):
    if request.method == "POST":
        product = AuctionListing.objects.get(pk=product_id)
        item_to_delete = Watchlist.objects.get(products=product, user=request.user)
        item_to_delete.delete()
        return redirect("watchlist")


def category_list(request):
    return render(
        request, "auctions/category.html", {"categories": Category.objects.all()}
    )


def search_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    products = category.auction_category.all()
    return render(request, "auctions/index.html", {"products": products})


def comment(request, product_id):
    if request.method == "POST":
        product = AuctionListing.objects.get(pk=product_id)
        comment_content = request.POST["comment"]
        owner = request.user
        Comment.objects.create(
            user=owner, auction_listing=product, comment=comment_content
        )
        return redirect("listing", product_id=product_id)
