from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from .models import Post
from django.contrib import messages

# blog/views.py
def home(request):
    return HttpResponse("Welcome to my blog!")

def home(request):
    return render(request, 'blog/home.html')

def home(request):
    posts = Post.objects.all().order_by('-created_at') # Latest Posts
    return render(request, 'blog/home.html', {'posts': posts})

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Post created successfully!")
            return redirect('home')  # change to your homepage name
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form, 'title': 'Create Post', 'button_text': 'Publish'})

def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form, 'title': 'Edit Post', 'button_text': 'Update'})

def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('home')
    return render(request, 'blog/delete_post.html', {'post': post})
