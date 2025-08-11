# blog_api/views.py
from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets
from blog.models import Post
from .serializers import PostSerializer, RegisterSerializer
from django.db import models  # Q objects ke liye
from .permissions import IsOwnerOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD for Blog Posts
    - Public posts for everyone
    - Private posts only for owner
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Post.objects.filter(
                models.Q(is_private=False) | models.Q(author=user)
            ).order_by('-created_at')
        return Post.objects.filter(is_private=False).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer