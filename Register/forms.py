from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomerRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your Username'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your Email'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your Password1'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your Password2'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



from django import forms
from .models import FoodItem,Billing

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'price','quantity']

# forms.py

class BillingForm(forms.ModelForm):
    mobile_number = forms.CharField(max_length=15, required=True)  # Add mobile number field

    class Meta:
        model = Billing
        fields = ['address', 'city', 'state', 'zip_code', 'mobile_number']  # Include other necessary fields
