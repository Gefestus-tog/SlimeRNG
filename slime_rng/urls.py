from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'slimes', views.SlimeTypeViewSet)
router.register(r'crafts', views.CraftRecipeViewSet)
router.register(r'collections', views.CollectionViewSet)

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    path('inventory/', views.PlayerInventoryView.as_view(), name='inventory'),
    path('craft/<int:recipe_id>/', views.CraftItemView.as_view(), name='craft'),
    path('claim-collection/<int:collection_id>/', views.ClaimCollectionView.as_view(), name='claim-collection'),
    path('save/', views.SaveGameView.as_view(), name='save-game'),
    path('load/', views.LoadGameView.as_view(), name='load-game'),
    
    path('', include(router.urls)),
]