from django.db import models

class Item_Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Create your models here.
class Item(models.Model):
    # Item id
    id = models.AutoField(primary_key=True)

    # Item details
    name = models.CharField(max_length=255)
    descriptions = models.TextField()
    quantity = models.IntegerField()
    category = models.ForeignKey(Item_Category, on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to=f'uploads/{id}/', null=False)

    def __str__(self):
        return self.name
