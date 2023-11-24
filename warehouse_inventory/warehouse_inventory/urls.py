"""
URL configuration for warehouse_inventory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from inventory import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.item_list, name="main"),
    path("item/<int:item_id>", views.individual_item, name="item"),
    path("add", views.add_item, name="add_item"),
    path("login", views.user_login, name="user_login"),
    path("logout", views.user_logout, name="user_logout"),
    path('items/<int:item_id>/delete/', views.delete_item, name='delete_item'),
    path('items/<int:item_id>/update/', views.update_item, name='update_item'),
    path('export-csv/', views.export_items_csv, name="export_items_csv")
]

# For serving media file in development ONLY.
# Don't use for production.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
