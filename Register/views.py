'''
    
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import CustomerRegisterForm, FoodItemForm
from .models import FoodItem

def home(request):
    return render(request, 'myapp/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = CustomerRegisterForm()
    return render(request, 'myapp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('condent')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'myapp/login.html')

@login_required
def condent(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.user = request.user
            food_item.save()
            return redirect('condent')
    else:
        form = FoodItemForm()

    items = FoodItem.objects.filter(user=request.user)
    total_amount = sum(item.price for item in items)

    return render(request, 'myapp/condent.html', {'form': form, 'items': items, 'total_amount': total_amount})

@login_required
def delete_item(request, item_id):
    if request.method == 'DELETE':
        item = FoodItem.objects.get(id=item_id, user=request.user)
        item.delete()
        return JsonResponse({'message': 'Item deleted successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

'''
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
from .forms import CustomerRegisterForm, FoodItemForm
from .models import FoodItem
from .forms import FoodItemForm, BillingForm
from .models import FoodItem, Order, Billing
from django.core.mail import send_mail


def home(request):
    return render(request, 'myapp/home.html')

def about(request):
    return render(request, 'myapp/about.html')


def contact(request):
    return render(request,"myapp/contact.html")

def register(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = CustomerRegisterForm()
    return render(request, 'myapp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('condent')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'myapp/login.html')

@login_required
def condent(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.user = request.user
            food_item.save()
            return redirect('condent')
    else:
        form = FoodItemForm()

    items = FoodItem.objects.filter(user=request.user)
    total_amount = sum(item.price * item.quantity for item in items)

    if 'generate_pdf' in request.GET:
        # Generate PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []

        # Title
        elements.append(Table([[f"UserName: {request.user.username}"]], colWidths=[6 * inch]))
        elements[-1].setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.grey), ('TEXTCOLOR', (0, 0), (-1, -1), colors.white), ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, -1), 14), ('BOTTOMPADDING', (0, 0), (-1, -1), 12)]))

        # Table data
        data = [["Item Name", "Price"]]
        for item in items:
            data.append([item.name, f"${item.price:.2f}"])
        data.append(["Total Amount", f"${total_amount:.2f}"])

        table = Table(data, colWidths=[4 * inch, 2 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.skyblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)

        doc.build(elements)

        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

    return render(request, 'myapp/condent.html', {'form': form, 'items': items, 'total_amount': total_amount})

@login_required
def delete_item(request, item_id):
    if request.method == 'DELETE':
        item = FoodItem.objects.get(id=item_id, user=request.user)
        item.delete()
        return JsonResponse({'message': 'Item deleted successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def create_order(request):
    items = FoodItem.objects.filter(user=request.user)
    if request.method == 'POST':
        total_amount = sum(item.price for item in items)
        order = Order.objects.create(user=request.user, total_amount=total_amount)
        order.items.set(items)
        order.save()
        return redirect('order_list')
    return render(request, 'myapp/create_order.html', {'items': items})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    username = request.user.username
    return render(request, 'myapp/order_list.html', {'orders': orders, 'username': username})

@login_required
def delete_order(request, order_id):
    if request.method == 'POST':
        order = Order.objects.get(id=order_id, user=request.user)
        order.delete()
        messages.success(request, 'Order deleted successfully.')
        return redirect('order_list')
    return JsonResponse({'error': 'Invalid request'}, status=400)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order
from .forms import BillingForm

@login_required
def billing_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            billing = form.save(commit=False)
            billing.order = order  # Ensure you set the order
            billing.user = request.user  # Ensure you set the user
            billing.save()

            # Optionally, you can send an email or perform other actions here

            messages.success(request, 'Billing details submitted successfully.')
            return redirect('condent')  # Ensure 'condent' is a valid URL name in your URLs config
    else:
        # Initialize the form with current user data, if needed
        initial_data = {}
        if hasattr(request.user, 'profile'):
            initial_data['mobile_number'] = request.user.profile.mobile_number
        form = BillingForm(initial=initial_data)

    return render(request, 'myapp/billing_detail.html', {'form': form, 'order': order})
