from django.contrib import admin
from .models import Laboratorio, Programa, Coordinador

@admin.register(Programa)
class ProgramaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'siglas', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'siglas')

@admin.register(Laboratorio)
class LaboratorioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'siglas')
    list_filter = ()
