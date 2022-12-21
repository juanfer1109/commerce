from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


def index(request):
    categories = Category.objects.all()
    if request.method == "POST":
        cat = request.POST['category']
        try:
            category = Category.objects.get(catName=cat)
        except:
            activeListing = Listing.objects.filter(is_active=True)
            return render(request, "auctions/index.html", {
                'listings':activeListing,
                'categories':categories
            })
        activeListing = Listing.objects.filter(is_active=True, category=category)
        return render(request, "auctions/index.html", {
        'listings':activeListing,
        'categories':categories
    })    
    activeListing = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        'listings':activeListing,
        'categories':categories
    })

def detailListing(request, pk):
    message_error = None
    message_ok = None
    winner = False
    listing = Listing.objects.get(pk=pk)
    isWatch = request.user in listing.watch.all()
    bids = Bid.objects.filter(listing=listing)
    allComments = Comment.objects.filter(listing=listing)
    cant_bids = len(bids)
    max_bid = 0
    if cant_bids > 0:
        for bid in bids:
            if bid.bid > max_bid:
                user_winner = bid.user
                max_bid = bid.bid
        if user_winner == request.user and listing.is_active == False:
            winner = True

    owner = False
    if request.method == 'POST':
        try:
            is_active = request.POST['is_active']
            if is_active == 'True':
                listing.is_active = False
                listing.save()
                return HttpResponseRedirect(reverse("index"))
        except:
            pass

        try:
            new_bid = float(request.POST['new_bid'])
            if listing.is_active == False:
                    return render(request, "auctions/detail.html", {
                        "element": listing,
                        "isWatch": isWatch,
                        "comments": allComments,
                        "owner": owner,
                        "message_error": message_error,
                        "message_ok": message_ok,
                        "cant_bids": cant_bids,
                        "winner": winner,
                        "max_bid": max_bid,
                    })
            else:
                if new_bid < listing.starting_bid:
                    message_error = "New BID must be at least the starting BID"
                else:
                    check = True
                    for bid in bids:
                        if new_bid <= bid.bid:
                            message_error = "New BID must be greater than actual BIDs"
                            check = False
                    if check:
                        bidNew = Bid(
                            user = request.user,
                            listing = listing,
                            bid = new_bid
                        )
                        bidNew.save()
                        message_ok = "New BID placed"
                        cant_bids += 1

        except:
            pass

        return render(request, "auctions/detail.html", {
            "element": listing,
            "isWatch": isWatch,
            "comments": allComments,
            "owner": owner,
            "message_error": message_error,
            "message_ok": message_ok,
            "cant_bids": cant_bids,
            "winner": winner,
            "max_bid": max_bid,
        })
        
    else:
        if request.user == listing.user:
            owner = True

        
        return render(request, "auctions/detail.html", {
            "element": listing,
            "isWatch": isWatch,
            "comments": allComments,
            "owner": owner,
            "message_error": message_error,
            "message_ok": message_ok,
            "cant_bids": cant_bids,
            "winner": winner,
            "max_bid": max_bid,
        })

def removeWatch(request, pk):
    listing = Listing.objects.get(pk=pk)
    actUser = request.user
    listing.watch.remove(actUser)
    return HttpResponseRedirect(reverse("detail", args=(pk, )))

def addWatch(request, pk):
    listing = Listing.objects.get(pk=pk)
    actUser = request.user
    listing.watch.add(actUser)
    return HttpResponseRedirect(reverse("detail", args=(pk, )))


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

def createListing(request):
    if request.method == "POST":
        actUser = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        starting_bid = request.POST["bid"]
        category = request.POST["category"]
        catInfo = Category.objects.get(catName=category)
        newListing = Listing(
            title=title,
            description=description,
            image_url=image_url,
            category=catInfo,
            user=actUser,
            starting_bid=starting_bid,
        )
        newListing.save()
        return HttpResponseRedirect(reverse(index))

    categories = Category.objects.all()
    return render(request, "auctions/create_listing.html", {
        'categories': categories
    })

def watchList(request):
    actUser = request.user
    activeListing = actUser.watch.all()
    return render(request, "auctions/watchlist.html", {
        'listings':activeListing,
    })    

def addComment(request, pk):
    author = request.user
    listing = Listing.objects.get(pk=pk)
    n_comment = request.POST['new_comment']

    new_comment = Comment(
        author=author,
        listing=listing,
        comment=n_comment
    )

    new_comment.save()

    return HttpResponseRedirect(reverse("detail", args=(pk, )))
