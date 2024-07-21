from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import CustomUser , Collection
from django.utils.translation import gettext_lazy as _


class CollectionInline(admin.TabularInline):
    model = Collection
    extra = 1  # Number of empty collection forms to display

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Manager info'), {'fields': ('manager_id', 'status')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'manager_id', 'status')}
        ),
    )
    list_display = ('username', 'first_name', 'last_name', 'email', 'status', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'status')
    list_filter = ('status', 'is_staff', 'is_superuser', 'is_active', 'groups')
    inlines = [CollectionInline]

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Collection)