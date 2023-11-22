from django.shortcuts import render, redirect
from .models import Item
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# List all the items here
@login_required(login_url='/login')
def item_list(request):
    items = Item.objects.all()
    return render(request, "main.html", {'items': items})

# User login
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "login successful")
            return redirect("/")
        else:
            messages.error(request, "Invalid login")

    return render(request, "login.html")

# User logout
def user_logout(request):
    logout(request)
    messages.success(request, "logout successful")
    return redirect("/login")

