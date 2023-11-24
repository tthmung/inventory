from django.db import models
from django import forms

# Categories, this allow for expanding of categories
class Item_Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Item model
class Item(models.Model):
    # Item id
    id = models.AutoField(primary_key=True)

    # Item details
    name = models.CharField(max_length=255)
    descriptions = models.TextField()
    quantity = models.IntegerField()
    # This is category_id in the database
    category = models.ForeignKey(Item_Category, on_delete=models.DO_NOTHING)
    # This is VARCHAR(100)
    image = models.ImageField(upload_to=f'uploads/{id}/', null=False)

    def __str__(self):
        return self.name

# Model form. Used for adding and updating
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'descriptions', 'quantity', 'category', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
