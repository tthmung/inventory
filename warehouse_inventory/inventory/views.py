from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, ItemForm, Item_Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
            return redirect("/")
        else:
            messages.error(request, "Error adding item")
            print(form.errors)

    categories = Item_Category.objects.all()
    return render(request, "form.html", {"categories": categories, "Update": False})

# Update item, work on privilege later
@user_passes_test(is_super_user, redirect_field_name="/")
def update_item(request, item_id):

    item = get_object_or_404(Item, pk=item_id)
    # Get the item we want to update
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            new_image = form.cleaned_data.get('image')
            # Delete the old picture if new image is provided
            if new_image:
                image_path = os.path.join(settings.MEDIA_ROOT, str(item.image))
                if os.path.exists(image_path):
                    os.remove(image_path) # Delete the image file
            form.save()
            messages.success(request, "Item updated successfully")
            return redirect(f'/item/{item_id}')
        else:
            messages.error(request, "Error updating item")
            print(form.errors)

    categories = Item_Category.objects.all()
    return render(request, "form.html", {"categories": categories, "item": item, "Update": True})

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

# Update quantity only
@login_required(login_url='/login')
def update_quantity(request, item_id, action):

    # Get the item that we want to update
    item = get_object_or_404(Item, pk=item_id)

    # Depending on the type add or subtract from existing item
    if action == "Take":
        item.quantity = item.quantity - int(request.POST[f'{item_id}_quantity_take'])
    else:
        item.quantity = item.quantity + int(request.POST[f'{item_id}_quantity_add'])

    item.save()

    # Refresh the item page
    messages.success(request, "Successful updated item")
    return redirect(f'/item/{item_id}')
