from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, ItemForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import os
from django.conf import settings

# List all the items here
@login_required(login_url='/login')
def item_list(request):
    items = Item.objects.all()
    return render(request, "main.html", {'items': items})

# List individual item
@login_required(login_url='/login')
def individual_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, "item.html", {"item": item})

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

# Delete an item, implement user privilege later
@require_http_methods("DELETE")
def delete_item(request, item_id):

    # Get the item with following item_id
    item = get_object_or_404(Item, pk=item_id)

    # Delete the picture associated with the item
    if item.image:
        image_path = os.path.join(settings.MEDIA_ROOT, str(item.image))
        if os.path.exists(image_path):
            os.remove(image_path) # Delete the image file

    # Delete the item
    item.delete()
    messages.success(request, "DELETE item successful")
    return redirect("/")

# Add an item, will add privilege later
@require_http_methods("POST")
def add_item(request):
    form = ItemForm(request.POST, request.FILES)
    if form.is_valid():
        # Save item if form is valid
        item = form.save()
        messages.success(request, "Item added successfully")
    else:
        messages.error(request, "Error adding item")

    return redirect("/")

# Update item, work on privilege later
@require_http_methods("UPDATE")
def update_item(request, item_id):

    # Get the item we want to update
    item = get_object_or_404(Item, pk=item_id)
    form = ItemForm(request.POST, request.FILES, instance=item)

    if form.is_valid():
        # Save the item if form is valid
        form.save()
        messages.success(request, "Item updated successfully")
    else:
        messages.error(request, "Error updating item")

    return redirect("/")

# Adding item to session storage


# Deleting item to session storage
