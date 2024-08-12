from django.db import models
# product/models.py

# product/models.py
from django.db import models

class VegetableProduct(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    kilogram = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='vegetable_products/', blank=True, null=True)  # Add this field

    def __str__(self):
        return self.name
