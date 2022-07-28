from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = ((
        (None, {
            'fields': ('email', 'password'),
        }),
        ('details', {
            'fields': ('phone', 'username', 'is_seller', 'status')
        }),
    ))
    add_fieldsets = ((
        None, {
            'fields': ('email', 'password1', 'password2', 'is_seller', 'status')
        }
    ),)
    list_display = [
        'username',
        'phone',
        'email',
        'is_superuser',
    ]

admin.site.register(CustomUser, CustomUserAdmin)