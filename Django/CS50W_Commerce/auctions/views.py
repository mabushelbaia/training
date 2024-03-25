from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from httplib2 import Http

from .models import Comment, Listing, User
from django.contrib.auth.decorators import login_required


def index(request):
    listings = Listing.objects.all().filter(status=True)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "mtitle": "Active Listings"
    })

def closed(request):
    listings = Listing.objects.all().filter(status=False)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "mtitle": "Closed Listings"
    })
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
class NewListingForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description")
    bid = forms.DecimalField(label="Starting Bid", min_value=0)
    category = forms.CharField(label="Category")
    image = forms.URLField(label="Image URL")

@login_required
def create(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["bid"]
            category = form.cleaned_data["category"]
            image = form.cleaned_data["image"]
            new_listing = Listing(title=title, description=description, price=price, category=category, image=image, user=request.user)
            new_listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })
    else:
        return render(request, "auctions/create.html", {
            "form": NewListingForm()
        })


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comments = Comment.objects.all().filter(listing=listing)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "in_wishlist": request.user.wishlist.filter(listing=listing).exists(),
        "comments": comments
    })

@login_required
def wishlist(request, listing_id=0):
    # check if if it is a remove or add request
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        user = request.user
        # check if the listing is already in the wishlist
        if user.wishlist.filter(listing=listing).exists():
            user.wishlist.filter(listing=listing).delete()
        else:
            user.wishlist.create(listing=listing)
        return HttpResponseRedirect(reverse("index"))
    else:
        listings = [wl.listing for wl in request.user.wishlist.all()]
        return render(request, "auctions/index.html",{
            "mtitle": "Wishlist",
            "listings": listings,
        })

@login_required
def close(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.status = False
    listing.save()
    return HttpResponseRedirect(reverse("index"))


@login_required
def bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        bid = int(request.POST["bid"])
        if bid > listing.price:
            listing.price = bid
            listing.highest_bidder = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": "Bid must be higher than the current bid."
            })
        

def categories(request):
    categories = Listing.objects.values_list('category', flat=True).distinct()
    print(categories)
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category):
    listings = Listing.objects.all().filter(category=category)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "mtitle": category
    })
def comment(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        comment = request.POST["comment"]
        new_comment = Comment(user=request.user, listing=listing, comment=comment)
        new_comment.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        return HttpResponseRedirect(reverse("index"))