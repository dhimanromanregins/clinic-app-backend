from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile,Banner, Notifications


class CustomUserAdmin(UserAdmin):
    # Display all fields in the admin list view
    list_display = (
        'first_name',
        'last_name',
        'phone_number',
        'id_number',
        'is_parent',
        'is_child',
        'is_active',
        'is_staff',
        'is_superuser',
        'device_token',
    )

    # Enable search functionality for all relevant fields
    search_fields = (
        'first_name',
        'last_name',
        'phone_number',
        'id_number',
        'device_token',
    )

    # Add filters for boolean and categorical fields
    list_filter = (
        'is_parent',
        'is_child',
        'is_active',
        'is_staff',
        'is_superuser',
    )

    # Customize the form layout
    fieldsets = (
        (None, {
            'fields': ('phone_number', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'id_number', 'device_token')
        }),
        ('Permissions', {
            'fields': ('is_parent', 'is_child', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login',)
        }),
    )

    # Fields to be displayed when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'id_number', 'first_name', 'last_name', 'password1', 'password2', 'is_parent', 'is_child', 'is_staff', 'is_superuser'),
        }),
    )

    ordering = ('phone_number',)


# Register the CustomUser model with the customized admin class
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Profile)
admin.site.register(Banner)
admin.site.register(Notifications)
