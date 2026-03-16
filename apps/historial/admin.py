from django.contrib import admin
from .models import Registro


@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'usuario', 'accion', 'modulo', 'descripcion', 'ip')
    list_filter = ('accion', 'modulo', 'fecha')
    search_fields = ('descripcion', 'modulo', 'usuario__username')
    readonly_fields = ('usuario', 'accion', 'modulo', 'descripcion', 'fecha', 'ip')
