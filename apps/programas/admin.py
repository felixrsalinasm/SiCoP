from django.contrib import admin
from .models import Laboratorio, Programa, Coordinador

@admin.register(Laboratorio)
class LaboratorioAdmin(admin.ModelAdmin):
    list_display = ('siglas', 'nombre', 'jefe')
    search_fields = ('nombre', 'siglas')

@admin.register(Programa)
class ProgramaAdmin(admin.ModelAdmin):
    list_display = ('siglas', 'nombre', 'nivel', 'activo')
    list_filter = ('nivel', 'activo')

@admin.register(Coordinador)
class CoordinadorAdmin(admin.ModelAdmin):
    list_display = ('profesor', 'programa', 'fecha_inicio', 'fecha_fin', 'es_actual')
    list_filter = ('programa',)
