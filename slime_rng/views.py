from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def set_cookie_view(request):
    response = HttpResponse("Куки установлены!")
    response.set_cookie(
        key="username",
        value="john_doe",
        max_age=3600 * 24 * 7,
        secure=True,      # Только по HTTPS
        httponly=True,    # Не доступно JS
        samesite='Lax'
    )
    return response

def read_cookie_view(request):
    username = request.COOKIES.get("username", "Гость")
    return HttpResponse(f"Привет, {username}!")

def delete_cookie_view(request):
    response = HttpResponse("Куки удалены!")
    response.delete_cookie("username")
    return response
