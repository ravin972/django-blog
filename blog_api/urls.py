# blog_api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),  # Auto URLs from router
     # Signup
    path('auth/register/', RegisterView.as_view(), name='api-register'),

    # Login -> returns {"access": "...", "refresh": "..."}
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Refresh access token
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
