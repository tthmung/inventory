from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, ItemForm, Item_Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import os
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse

# Check if a user is a super user.
# Super user (called staff_user in admin) can only add and delete items.
# Regular user can only update items.
def is_super_user(user: User) -> bool:
    return user.is_authenticated and user.has_perm("inventory.add_item")

# List all the items here
@login_required(login_url='/login')
def item_list(request):
    items = Item.objects.all()
    return render(request, "main.html", {'items': items, 'super_user': is_super_user(request.user)})

# List individual item
@login_required(login_url='/login')
def individual_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, "item.html", {"item": item, 'super_user': is_super_user(request.user)})

# Render the form page, only accessible to admin and super user
@user_passes_test(is_super_user)
def render_form(request):
    return render(request, "form.html")

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

# Delete an item only if user is super_user
@user_passes_test(is_super_user)
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

# Add an item only if user is super user
@user_passes_test(is_super_user, redirect_field_name="/")
def add_item(request):

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            # Save item if form is valid
            form.save()
            messages.success(request, "Item added successfully")
        else:
            messages.error(request, "Error adding item")

        return redirect("/")

    categories = Item_Category.objects.all()
    return render(request, "form.html", {"categories": categories})

# Update item, work on privilege later
@login_required(login_url='/login')
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

# Export all items to csv
@login_required(login_url='/login')
def export_items_csv(request):

    # Make ready for download, will be named items.csv
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="items.csv"'

    import csv
    # Create a csv file with the following headers
    writer = csv.writer(response)
    writer.writerow(["ID", "Name", "Descriptions", "Quantity", "Category", "Picture URL"])

    # Get all items and add line by line
    items = Item.objects.all()
    for item in items:
        writer.writerow([item.id, item.name, item.descriptions, item.quantity, item.category, item.image.url])

    messages.success(request, "Successfully exported to csv")
    return response
