from django.db import models
from django.contrib.auth.models import User

class FoodItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - Rs {self.price}'

    @property
    def total_value(self):
        return self.price

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(FoodItem)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class Billing(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    billing_date = models.DateTimeField(auto_now_add=True)
    billing_address = models.TextField()

    def __str__(self):
        return f"Billing for Order {self.order.id}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)

# Ensure the profile is created/updated whenever the user is saved
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

# models.py
# models.py
from django.db import models
from django.conf import settings

class Billing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, default='Unknown Address')
    city = models.CharField(max_length=100, default='Unknown City')
    state = models.CharField(max_length=100, default='Unknown State')
    zip_code = models.CharField(max_length=20, default='00000')
    mobile_number = models.CharField(max_length=15, default='0000000000')

    def __str__(self):
        return f"Billing details for {self.user.username}"
