# blog_api/urls.py
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import PostListCreateView, PostRetrieveUpdateDestroyView

urlpatterns = [
    # Get token: POST {username, password} -> {"token": "..."}
    path('user/login/', obtain_auth_token, name='api-token-login'),

    # Posts (private)
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
]
