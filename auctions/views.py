from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Listing, Comment, Bid







def index(request):
    listing = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "list_of_listings": listing
    })



def create_listing(request):
    if request.method == 'POST':
        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        starting_bid = request.POST["starting_bid"]
        category = request.POST["category"]
        owner = request.user
        if image_url == "":
            image_url = "https://static.vecteezy.com/system/resources/thumbnails/004/141/669/small/no-photo-or-blank-image-icon-loading-images-or-missing-image-mark-image-not-available-or-image-coming-soon-sign-simple-nature-silhouette-in-frame-isolated-illustration-vector.jpg"
        category = Category.objects.get(category_name=category)
        new_listing = Listing(title=title, description=description, image_url=image_url, current_bid=starting_bid, owner=owner, category=category)
        new_listing.save()
        return HttpResponseRedirect(reverse(index))
    else:
        list_of_categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": list_of_categories
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
    

def all_category_view(request):
    return render(request, "auctions/category_home.html", {
        "categories": Category.objects.all()
    })

def category_view(request, category_name):
    category_name = Category.objects.get(category_name=category_name)
    list_of_listings = Listing.objects.filter(category=category_name, is_active=True)
    if str(list_of_listings) == "<QuerySet []>":
        list_of_listings = None
    return render(request, "auctions/category.html", {
        "category": category_name,
        "list_of_listings": list_of_listings
    })
    
def listing_view(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.user in listing.watchlist.all():
        watchlist = True
    else:
        watchlist = False
    comments = Comment.objects.filter(comment_listing=listing)
    bids_now = len(Bid.objects.filter(bid_listing=listing))
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "in_watchlist": watchlist,
        "comments": comments,
        "bids_now": bids_now
    })

def remove_watchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.watchlist.remove(request.user)
    return HttpResponseRedirect(reverse("listing_view", args=(listing_id, )))

def add_watchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.watchlist.add(request.user)
    return HttpResponseRedirect(reverse("listing_view", args=(listing_id, )))


def watchlist_view(request):
    watchlist = request.user.watchlist.all()
    if str(watchlist) == "<QuerySet []>":
        watchlist = None
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

def edit_listing(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        listing.title = request.POST["title"]
        listing.description = request.POST["description"]
        listing.image_url = request.POST["image_url"]
        listing.starting_bid = request.POST["starting_bid"]
        category = request.POST["category"]
        listing.owner = request.user
        if listing.image_url == "":
            listing.image_url = "https://static.vecteezy.com/system/resources/thumbnails/004/141/669/small/no-photo-or-blank-image-icon-loading-images-or-missing-image-mark-image-not-available-or-image-coming-soon-sign-simple-nature-silhouette-in-frame-isolated-illustration-vector.jpg"
        listing.category = Category.objects.get(category_name=category)
        listing.save()
        return HttpResponseRedirect(reverse(index))
    else:
        listing = Listing.objects.get(id=listing_id)
        if listing.owner == request.user:
            return render(request, "auctions/edit_page.html", {
                "listing": listing,
                "categories": Category.objects.all()
            })
        else:
            return HttpResponseRedirect(reverse('index'))
    
def comment(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.method == 'POST':

        new_comment = Comment(comment_author=request.user, comment_listing=listing, comment_content=request.POST["comment_content"])
        new_comment.save()
        return HttpResponseRedirect(reverse('listing_view', args=(listing_id, ) ))
    else:
        return HttpResponseRedirect(reverse('listing_view', args=(listing_id, ) )) 
    
def bid(request, listing_id):

    if request.method == 'POST':
        bid_value = float(request.POST["bid_value"])
        listing = Listing.objects.get(id=listing_id)
        if listing.current_bid < bid_value:
            new_bid = Bid(bid=bid_value, bid_user=request.user, bid_listing=listing)
            new_bid.save()
            listing.current_bid = bid_value
            listing.save()
            if request.user in listing.watchlist.all():
                watchlist = True
            else:
                watchlist = False
            comments = Comment.objects.filter(comment_listing=listing)
            bids_now = len(Bid.objects.filter(bid_listing=listing))
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "in_watchlist": watchlist,
                "comments": comments,
                "bids_now": bids_now, 
                "alert": 1
            })
        else:
            if request.user in listing.watchlist.all():
                watchlist = True
            else:
                watchlist = False
            comments = Comment.objects.filter(comment_listing=listing)
            bids_now = len(Bid.objects.filter(bid_listing=listing))
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "in_watchlist": watchlist,
                "comments": comments,
                "bids_now": bids_now, 
                "alert": 2
            })

def closed_view(request):
    listing = Listing.objects.filter(is_active=False)
    return render(request, "auctions/closed.html", {
        "list_of_listings": listing
    })

def close_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    winning_bid = None
    for bid in Bid.objects.filter(bid=listing.current_bid, bid_listing=listing):
        winning_bid = bid
    if request.user in listing.watchlist.all():
        watchlist = True
    else:
        watchlist = False
    comments = Comment.objects.filter(comment_listing=listing)
    bids_now = len(Bid.objects.filter(bid_listing=listing))
    listing.is_active = False
    listing.save()
    return render(request, 'auctions/listing.html', {
        "listing": listing,
        "in_watchlist": watchlist,
        "comments": comments,
        "bids_now": bids_now, 
        "alert": 3,
        "winning_bid": winning_bid
    })

    