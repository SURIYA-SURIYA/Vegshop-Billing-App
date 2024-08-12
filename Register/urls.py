from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('condent/', views.condent, name='condent'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),    
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('create_order/', views.create_order, name='create_order'),
    path('order_list/', views.order_list, name='order_list'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('billing_detail/<int:order_id>/', views.billing_detail, name='billing_detail'),

]
