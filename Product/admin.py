from django.contrib import admin
from .models import VegetableProduct

# product/admin.py

# Incorrect: Duplicate registration
admin.site.register(VegetableProduct)
  # This should be removed
