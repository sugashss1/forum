from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Post, Reply
from django.contrib.auth.models import User


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        return render(request, 'login.html', {'msg': 'Invalid credentials'})
    return render(request, 'login.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if password!=confirm_password:
            return render(request, 'register.html',{'msg':'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'msg': 'Username taken'})
        user = User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'register.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):
    posts =reversed(Post.objects.all())
    return render(request, 'index.html', {'posts': posts})

@login_required
def my_posts(request,name):
    posts =Post.objects.filter(user=request.user).reverse()
    print(type(posts))
    total_posts=len(posts)
    total_likes=0
    for i in posts:
        total_likes+=i.no_likes
    
    return render(request, 'my_posts.html', {'posts': posts,"total_posts":total_posts,"total_likes":total_likes})

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Post.objects.create(title=title, content=content,user=request.user)
        return redirect('index')
    return redirect("index")

@login_required
def reply(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        reply = Reply.objects.create(content=content, post=post)
        post.replies.add(reply)
        return redirect('index')
    return redirect('index')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    if user in post.users_liked.all():
        post.users_liked.remove(user)
        post.no_likes -= 1
        post.save()
        return HttpResponse(f"""<button class="like-button"
                    hx-post="/like/{ post.id }"
                    hx-trigger="click"
                    hx-target="this"
                    hx-swap="outerHTML">
                    <span id="heartIcon" class="red_span">❤️</span>
                    <span id="like-count-{ post.id }" class="red_span">{ post.no_likes }</span>
                </button>""")
    else:
        post.users_liked.add(user)
        post.no_likes += 1
        post.save()
        return HttpResponse(f"""<button class="liked-button"
                    hx-post="/like/{ post.id }"
                    hx-trigger="click"
                    hx-target="this"
                    hx-swap="outerHTML">
                    <span id="heartIcon" class="red_span">❤️</span>
                    <span id="like-count-{ post.id }" class="red_span">{ post.no_likes }</span>
                </button>""")


