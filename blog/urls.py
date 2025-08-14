from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('explore/', views.explore, name='explore'),
    path('create/', views.create_post, name='create_post'),
    path('post/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('post/<slug:slug>/delete/', views.delete_post, name='delete_post'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
