from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass  

if User not in admin.site._registry:
    @admin.register(User)
    class CustomUserAdmin(admin.ModelAdmin):
        list_display = ("username", "email", "is_staff", "is_active")
