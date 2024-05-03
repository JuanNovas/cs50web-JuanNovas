from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.core.serializers import serialize
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Post, Followers, Likes


def index(request):
    twits = Post.objects.all()[::-1]
    paginator = Paginator(twits, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",{
        "page" : page_obj,
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
    
@csrf_exempt
@login_required
def new_post(request):
    
    if request.method == "POST":
        
    
        data = json.loads(request.body)
        body = data["twit"]
        
        if body == "":
            return JsonResponse({"error": "At least 1 caracter needed."}, status=400)
        
        twit = Post(user=request.user,body=body)
        twit.save()
        
        return JsonResponse({"message": "Posted succesfully."}, status=201)
        
    elif request.method == "PUT":
        data = json.loads(request.body)
        body = data["twit"]
        
        if body == "":
            return JsonResponse({"error": "At least 1 caracter needed."}, status=400)
        
        try:
            twit = Post.objects.get(user=request.user, id=data["id"])
        except Post.DoesNotExist:
            return JsonResponse({"error": "Twit not found."}, status=404)
        
        
        twit.body = body
        twit.save()
        return HttpResponse(status=204)
    
    return JsonResponse({"error": "Method not allowed."}, status=400)
        
        
        

def profile (request, username):
    user = User.objects.get(username=username)
    if user == None:
        return HttpResponseRedirect(reverse("index"))
    
    followers = Followers.objects.filter(followed=user).all()
    follows = Followers.objects.filter(follower=user).all()
    twitts = Post.objects.filter(user=user)[::-1]
    paginator = Paginator(twitts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        follow = Followers.objects.filter(follower=request.user, followed=user).exists()
    else:
        follow = False
    
    
    
    return render(request, "network/profile.html",{
        "prof_user" : user,
        "page" : page_obj,
        "follow" : follow,
        "follows_count" : follows.count(),
        "followers_count" : followers.count()
    })
    
@login_required
def follow(request, prof_username):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))
    
    prof_user = User.objects.get(username=prof_username)
    try:
        x = Followers.objects.get(follower=request.user, followed=prof_user)
        x.delete()
    except Followers.DoesNotExist:
        new_follower = Followers(follower=request.user, followed=prof_user)
        new_follower.save()

    return HttpResponseRedirect(reverse("profile", args=(prof_username,)))

@login_required
def following(request):
    users_followed = Followers.objects.filter(follower=request.user)
    users_followed = [followed.followed for followed in users_followed]
    users_followed.append(request.user)
    twits = Post.objects.filter(user__in=users_followed)[::-1]

    paginator = Paginator(twits, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",{
        "page" : page_obj,
    })
    
   
   
@csrf_exempt
@login_required 
def like(request):
    if request.method == "PUT":        
    

        data = json.loads(request.body)
        
        post = Post.objects.get(id=data["id"])
        
        try:
            x = Likes.objects.get(user=request.user, post=post)
            x.delete()
        except Likes.DoesNotExist:
            new_like = Likes(user=request.user, post=post)
            new_like.save()
            
        return HttpResponse(status=204)
    
    if request.method == "GET":
        
        id = request.GET.get('id', None)
        if id:
            post = Post.objects.get(id=id)
            data = {
                "state" : Likes.objects.filter(user=request.user, post = post).exists(),
                "amount" : post.likes_count()
            }
            return JsonResponse(data)
    
    
    return JsonResponse({"error": "Method not allowed."}, status=400)


@csrf_exempt
def like_button (request):
    id = request.GET.get('id', None)
    if id:
        post = Post.objects.get(id=id)
        data = {
            "state" : Likes.objects.filter(user=request.user, post = post).exists()
        }
        return JsonResponse(data)