from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .forms import PostForm
from .models import Post
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic import ListView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostSerializer

# blog/views.py
def home(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(
            Q(is_private=False) | Q(author=request.user)
        ).order_by('-created_at')
    else:
        posts = Post.objects.filter(is_private=False).order_by('-created_at')
    
    return render(request, 'blog/home.html', {'posts': posts})

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if post.is_private and post.author != request.user:
        return HttpResponseForbidden("You are not allowed to view this private post.")
    
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()  # This will automatically generate the slug
            messages.success(request, "Post created successfully!")
            return redirect('home')
    else:
        form = PostForm()
        
    # Add Bootstrap classes to form widgets
    form.fields['title'].widget.attrs.update({'class': 'form-control'})
    form.fields['content'].widget.attrs.update({'class': 'form-control'})
    form.fields['is_private'].widget.attrs.update({'class': 'form-check-input'})
    
    return render(request, 'blog/create_post.html', {'form': form, 'title': 'Create Post'})

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # ✅ Only allow post author to edit
    if request.user != post.author:
        messages.error(request, "You are not allowed to edit this post.")
        return redirect('home')

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form, 'title': 'Edit Post', 'button_text': 'Update'})

@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    # ✅ Only allow post author to delete
    if request.user != post.author:
        messages.error(request, "You are not allowed to delete this post.")
        return redirect('home')
    
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('home')
    return render(request, 'blog/delete_post.html', {'post': post})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to the blog!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form, 'title': 'Sign Up'})

@login_required
def dashboard(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/dashboard.html', {'posts': posts})

def explore(request):
    if request.user.is_authenticated:
        # Show all public posts except user's own posts
        posts = Post.objects.filter(is_private=False).exclude(author=request.user).order_by('-created_at')
    else:
        # Show all public posts
        posts = Post.objects.filter(is_private=False).order_by('-created_at')
    return render(request, 'blog/explore.html', {'posts': posts})

@login_required
def dashboard(request):
    posts = Post.objects.filter(author=request.user)

    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
            return redirect('dashboard')

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            return redirect('dashboard')
    else:
        user_form = UserChangeForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)

    return render(request, 'blog/dashboard.html', {
        'posts': posts,
        'user_form': user_form,
        'password_form': password_form,
    })

class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Show all public posts + user's private posts
            return Post.objects.filter(
                is_private=False
            ) | Post.objects.filter(
                is_private=True, author=user
            )
        else:
            # Only public posts for anonymous users
            return Post.objects.filter(is_private=False)

class PostListAPI(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)        