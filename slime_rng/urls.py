from django.urls import path
from . import views

urlpatterns = [
    path('set-cookie/', views.set_cookie_view, name='set_cookie'),
    path('read-cookie/', views.read_cookie_view, name='read_cookie'),
    path('delete-cookie/', views.delete_cookie_view, name='delete_cookie'),
] 