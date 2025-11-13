from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.core.paginator import Paginator

import json
from .models import User, Post, Like, UserFollow

def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":
        # Attempt to sign username
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


def posts(request):
    if not request.user.is_authenticated:
        return render(request, "network/register.html")
    
    if request.method == "POST":
        post_text = request.POST.get("post_text")
        if post_text:
            Post.objects.create(post_text=post_text, creator=request.user)

        return redirect('posts')
    
    posts = Post.objects.all().order_by('-date')
    user_liked_posts = list(request.user.user_likes.values_list("post_id", flat=True))
    pagination = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = pagination.get_page(page_number)

    return render(request, 'network/posts.html', {"user_liked_posts": user_liked_posts, "page_obj": page_obj}) 


def edit_post(request):
    if not request.user.is_authenticated:
        return render(request, "network/register.html")
    
    if request.method == "POST":
        data = json.loads(request.body)
        new_post_text = data.get("post_text")
        post_id = data.get("post_id")
         
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({'error': "Post does not exist"}, status=404)   

        if post.creator != request.user:
            return JsonResponse({'error': "You are not allowed to edit this post!"}, status=403)

    
        post.post_text = new_post_text
        post.save()

        return JsonResponse({'success': True, 'PostText': post.post_text})
    return JsonResponse({'error': "Invalid request"},status=400)    


def list_posts(request):
    if not request.user.is_authenticated:
        return render(request, "network/register.html")
    
    posts = Post.objects.all().order_by('-date')
    user_liked_posts = list(request.user.user_likes.values_list("post_id", flat=True))

    pagination = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = pagination.get_page(page_number)
    return render(request, "network/posts.html",{"user_liked_posts": user_liked_posts, "page_obj": page_obj})


def like_or_unlike(request):
    if not request.user.is_authenticated:
        return render(request, "network/register.html")
    
    data = json.loads(request.body)
    creator_id = data.get('creator_id')
    post_id = data.get('post_id')

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': "Post does not exist"}, status=404)   
    
    if Like.objects.filter(creator_id=creator_id, post_id=post_id).exists():
        Like.objects.filter(creator_id=creator_id, post_id=post_id).delete()
        return JsonResponse({'liked': False})
    else:
        Like.objects.create(creator_id=creator_id, post_id=post_id)
        return JsonResponse({'liked': True})


def following_user(request):
    if not request.user.is_authenticated:
        return render(request, "network/register.html")
        
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('userId')
        following_user_id = data.get('followingUserId')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': f"User '{user_id}' does not exist"}, status=404)   
        
        try:
            user_following = User.objects.get(id=following_user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': f"Following user '{following_user_id}' does not exist"}, status=404)   

        if UserFollow.objects.filter(user=user, user_following=user_following).exists():
             UserFollow.objects.filter(user=user, user_following=user_following).delete()
             return JsonResponse({'follow': False})
        else:
            UserFollow.objects.create(user=user, user_following=user_following)
            return JsonResponse({'follow': True})

    
def profile(request, creator_id):
    if not request.user.is_authenticated:
        return render(request, 'network/register.html')

    creator = User.objects.get(pk=creator_id)
    posts = Post.objects.filter(creator=creator_id).order_by('-date')
    user_liked_posts = list(request.user.user_likes.values_list("post_id", flat=True))

    is_following = UserFollow.objects.filter(user=request.user, user_following=creator).exists()

    pagination = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = pagination.get_page(page_number) 
    
    return render(request, 'network/profile.html', {'is_following': is_following, 'creator_id': creator_id, 'creator': creator, 'user_liked_posts': user_liked_posts, "page_obj": page_obj})


def follow(request):
    if not request.user.is_authenticated:
        return render(request, 'network/register.html')

    followings = UserFollow.objects.filter(user=request.user)
    followed_user_ids = followings.values_list("user_following", flat=True)
    posts = Post.objects.filter(creator__in=followed_user_ids).order_by('-date')
    user_liked_posts = list(request.user.user_likes.values_list("post_id", flat=True))

    pagination = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = pagination.get_page(page_number)

    return render(request, 'network/following.html', {'user_liked_posts': user_liked_posts, 'page_obj':page_obj})


