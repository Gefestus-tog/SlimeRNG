from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views



urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    path('save/', views.SaveGameView.as_view(), name='save-game'),
    path('load/', views.LoadGameView.as_view(), name='load-game'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    
]