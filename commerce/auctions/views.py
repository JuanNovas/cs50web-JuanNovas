from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Auction, Watchlist, Bids, Comments

class NewListing(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewListing, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['image'].required = False
        self.fields['category'].required = False
    
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    
    class Meta:
        model = Auction
        fields = ['name', 'description', 'start_bid', 'image', 'category']
    
    def clean_start_bid(self):
        bid = self.cleaned_data.get('start_bid')
        
        if bid <= 0:
            raise forms.ValidationError("The start bid needs to be at least 1")
        
        return bid
       
       
all_categorys = (
    'Electronics',
    'Computers',
    'Smart Home',
    'Arts & Crafts',
    'Automotive',
    'Baby',
    'Beauty and Personal Care',
    "Women's Fashion",
    "Men's Fashion",
    "Girl's Fashion",
    "Boy's Fashion",
    'Health and Household',
    'Home and Kitchen',
    'Industrial and Scientific',
    'Luggage',
    'Movies & Television',
    'Pet Supplies',
    'Software',
    'Sports and Outdoors',
    'Tools & Home Improvement',
    'Toys and Games',
    'Video Games'
    )    

category_dic = {
    'Electronics': 'ELEC',
    'Computers': 'COMP',
    'Smart Home': 'SMH',
    'Arts & Crafts': 'ARTS',
    'Automotive': 'AUTO',
    'Baby': 'BABY',
    'Beauty and Personal Care': 'BEAUTY',
    "Women's Fashion": 'WOMEN',
    "Men's Fashion": 'MEN',
    "Girl's Fashion": 'GIRLS',
    "Boy's Fashion": 'BOYS',
    'Health and Household': 'HEALTH',
    'Home and Kitchen': 'HOME',
    'Industrial and Scientific': 'INDUSTRIAL',
    'Luggage': 'LUGGAGE',
    'Movies & Television': 'MOVIES',
    'Pet Supplies': 'PETS',
    'Software': 'SOFTWARE',
    'Sports and Outdoors': 'SPORTS',
    'Tools & Home Improvement': 'TOOLS',
    'Toys and Games': 'TOYS',
    'Video Games': 'VIDEOGAMES'
}   

def index(request):
    return render(request, "auctions/index.html", {
        "listings" : Auction.objects.all()
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

@login_required
def new_listing(request):
    if request.method == "POST":
        form = NewListing(request.POST)
        if form.is_valid():
            # Guardar el listado asociado al usuario actual
            new_listing = form.save(commit=False)
            new_listing.seller = request.user  # Acceder al usuario actual
            new_listing.save()
            return HttpResponseRedirect(reverse("index"))

            
        return render(request, "auctions/new_listing.html", {
            "form" : NewListing()
        })
    else:
        return render(request, "auctions/new_listing.html", {
            "form" : NewListing()
        })
        
def listing_page(request, item):
    item_object = Auction.objects.filter(name=item).first()

    if request.method == "POST":
        action = request.POST["watchlbutton"]
        if action == "add":
            if not Watchlist.objects.filter(user=request.user, post=item_object.id).first():
                new_watchlist = Watchlist(user=request.user, post=Auction.objects.get(name=item))
                new_watchlist.save()
        elif action == "remove":
            item_object = Auction.objects.get(name=item)
            if Watchlist.objects.filter(user=request.user, post=item_object.id).first():
                watchlist_delete = Watchlist.objects.filter(user=request.user, post=item_object.id).first()
                watchlist_delete.delete()
          
        if Watchlist.objects.filter(user=request.user, post=item_object.id).first():
            in_watchlist = True
        else:
            in_watchlist = False
                
        return render(request, "auctions/listing_page.html", {
            "item" : item_object,
            "in_watchlist" : in_watchlist,
            "comments" : Comments.objects.filter(post=item_object.id)
        })
        
    else:
        try:
            if Watchlist.objects.filter(user=request.user, post=item_object.id).first():
                in_watchlist = True
            else:
                in_watchlist = False
                
            comments = Comments.objects.filter(post=item_object.id)
        except:
            in_watchlist = False
            comments = []
        return render(request, "auctions/listing_page.html", {
            "item" : item_object,
            "in_watchlist" : in_watchlist,
            "comments" : comments
        })
        
@login_required
def make_bid(request, item):
    if request.method == "POST":
        item_object = Auction.objects.filter(name=item).first()
        amount = int(request.POST["bid_amount"])
        if amount > item_object.start_bid or amount == item_object.start_bid and Bids.objects.filter(post=item_object).first() == None:
            # Delete last bid log 
            last_bid = Bids.objects.filter(post=item_object).first()
            if last_bid:
                last_bid.delete()
            # Creating new bid log
            new_object = Bids(user=request.user, post=item_object)
            new_object.save()
            # Updating bid amount
            item_object.start_bid = amount
            # Updating bid bidder
            item_object.bidder = request.user
            item_object.save()
            return HttpResponseRedirect(reverse("listing page", kwargs={"item" : item}))
    else:
        return HttpResponseRedirect(reverse("index"))
    
    
def delete_auction(request, item):
    if request.method == "POST":
        item_object = Auction.objects.filter(name=item).first()
        if item_object != None and item_object.seller == request.user:
            item_object.active = False
            item_object.save()
    
    return HttpResponseRedirect(reverse("index"))

@login_required
def new_comment(request, item):
    if request.method == "POST":
        new_comment_text = request.POST["new_comment"]
        new_object = Comments(user=request.user, post=Auction.objects.filter(name=item).first(), comment=new_comment_text)
        new_object.save()
        
    return HttpResponseRedirect(reverse("listing page", kwargs={"item" : item}))
        
        
@login_required
def watchlist(request):

    return render(request,"auctions/watchlist.html",{
        "items" : Watchlist.objects.filter(user=request.user)
    })
    
    
def categorys(request,category=None):
    
    try:
        auctions = Auction.objects.filter(category=category_dic[category])
        
        if auctions == None:
            return render(request, "auctions/category_notfound.html")

        return render(request, "auctions/category.html",{
            "category" : category,
            "posts" : auctions
        })
    except:
        if category == None:
            return render(request, "auctions/category.html",{
            "categorys" : all_categorys
        })
            
        return render(request, "auctions/category_notfound.html")
