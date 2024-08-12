from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Unregister the original UserAdmin
admin.site.unregister(User)

# Define a custom UserAdmin (optional customization)
class CustomUserAdmin(UserAdmin):
    # Add any customizations here
    pass

# Register the custom UserAdmin
admin.site.register(User, CustomUserAdmin)

