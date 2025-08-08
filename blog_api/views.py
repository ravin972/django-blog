# blog_api/views.py
from rest_framework import generics, permissions
from blog.models import Post
from .serializers import PostSerializer

# List & Create — sirf logged-in user, list = only user's posts
class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # user apne posts hi dekhega
        return Post.objects.filter(author=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# Retrieve / Update / Delete — owner only (we restrict via queryset)
class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # only owner can retrieve/update/delete
        return Post.objects.filter(author=self.request.user)

class PublicPostListView(generics.ListAPIView):
    queryset = Post.objects.filter(is_private=False).order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]   # public
