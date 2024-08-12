from django import forms
from .models import VegetableProduct

class VegetableProductForm(forms.ModelForm):
    class Meta:
        model = VegetableProduct
        fields = ['name', 'price','kilogram','image']
