# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SystAdmin, SalesRep, Customer
from .forms import CustomUserCreationForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    list_display = ['email', 'username', 'user_role', 'is_staff', 'is_active']
    list_filter = ['user_role', 'is_staff', 'is_active']
    search_fields = ['email', 'username']
    ordering = ['email']
    
    # Customize the fieldsets to include email prominently
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Custom Fields', {'fields': ('user_role',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'user_role', 'password1', 'password2'),
        }),
    )

@admin.register(SystAdmin)
class SystAdminAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'phone_number', 'created_at']
    search_fields = ['user__email', 'user__username']

@admin.register(SalesRep)
class SalesRepAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'phone_number', 'created_at']
    search_fields = ['user__email', 'user__username']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'phone_number', 'created_at']
    search_fields = ['user__email', 'user__username']
