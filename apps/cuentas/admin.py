from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'rol', 'is_active')
    list_filter = ('rol', 'is_active')
    search_fields = ('username', 'email')
    readonly_fields = ('last_login', 'date_joined')
    fieldsets = UserAdmin.fieldsets + (
        ('Rol en SiCoP', {'fields': ('rol',)}),
    )
