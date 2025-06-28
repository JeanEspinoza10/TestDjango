from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SalesPerson

@admin.register(SalesPerson)
class SalesPersonAdmin(UserAdmin):
    model = SalesPerson
    list_display = ('email', 'name', 'is_admin', 'is_superuser', 'is_active')
    list_filter = ('is_admin','is_superuser')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('name',)}),
        ('Permisos', {'fields': ('is_admin', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_admin', 'is_active')}
        ),
    )