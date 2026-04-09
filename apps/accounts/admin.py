from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'phone', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')

    fieldsets = UserAdmin.fieldsets + (
        ('Hostel Info', {
            'fields': ('role', 'phone', 'parent_phone', 'institution', 'address', 'profile_pic')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Hostel Info', {
            'fields': ('role', 'phone', 'parent_phone', 'institution', 'address')
        }),
    )
