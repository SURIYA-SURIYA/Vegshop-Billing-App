# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .forms import VegetableProductForm
from .models import VegetableProduct
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import VegetableProduct


from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import VegetableProductForm
from .models import VegetableProduct

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:  # Ensure user is an admin
            login(request, user)
            return redirect('admin_dashboard')  # Redirect to admin dashboard
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid credentials'})
    return render(request, 'admin_login.html')

@login_required
@user_passes_test(lambda user: user.is_superuser)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
@user_passes_test(lambda user: user.is_superuser)
def add_vegetable_product(request):
    if request.method == 'POST':
        form = VegetableProductForm(request.POST)
        if form.is_valid():
            vegetable_product = form.save(commit=False)
            vegetable_product.created_by = request.user
            vegetable_product.save()
            messages.success(request, 'Vegetable product added successfully!')
            return redirect('list_vegetable_products')
    else:
        form = VegetableProductForm()
    return render(request, 'add_vegetable_product.html', {'form': form})

@login_required
@user_passes_test(lambda user: user.is_superuser)
def list_vegetable_products(request):
    products = VegetableProduct.objects.all()
    return render(request, 'list_vegetable_products.html', {'products': products})

@login_required
def list_vegetable_products(request):
    products = VegetableProduct.objects.all()
    return render(request, 'list_vegetable_products.html', {'products': products})