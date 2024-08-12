# urls.py

from django.urls import path
from .views import add_vegetable_product, list_vegetable_products
from . import views
from django.contrib.auth import views as auth_views

from .views import add_vegetable_product, list_vegetable_products  # Import your views



urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_vegetable_product/', add_vegetable_product, name='add_vegetable_product'),
    path('list_vegetable_products/', list_vegetable_products, name='list_vegetable_products'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Add this line

]
