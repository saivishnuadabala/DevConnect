
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post,Comment,Like

# Home Page
@login_required
def home(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "home.html", {"posts": posts})

# Create Post
@login_required
def create_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        image = request.FILES.get("image")  # Image upload
        Post.objects.create(user=request.user, content=content, image=image)
        return redirect("home")
    return render(request, "create_post.html")
# Register User
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")
    return render(request, "register.html")

# Login User
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")  # Redirect to homepage (to be created)
        else:
            messages.error(request, "Invalid username or password!")
    return render(request, "login.html")

# Logout User
def user_logout(request):
    logout(request)
    return redirect("login")


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like

# Like a Post
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:  # If already liked, unlike it
        like.delete()
    
    return redirect("home")

# Comment on a Post
@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == "POST":
        content = request.POST["content"]
        Comment.objects.create(user=request.user, post=post, content=content)
    
    return redirect("home")

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user == request.user:  # Ensure only the owner can delete
        post.delete()
    
    return redirect('home')
