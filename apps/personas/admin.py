from django.contrib import admin
from .models import Persona, Profesor, Estudiante

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'paterno', 'materno', 'email', 'creado_en')
    search_fields = ('nombres', 'paterno', 'rfc', 'email')
    list_filter = ('creado_en',)

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('persona', 'grado_academico', 'laboratorio', 'activo')
    list_filter = ('grado_academico', 'laboratorio', 'activo')
    search_fields = ('persona__nombres', 'persona__paterno')
    actions = ['marcar_activos', 'marcar_inactivos']

    @admin.action(description='Marcar seleccionados como activos')
    def marcar_activos(self, request, queryset):
        queryset.update(activo=True)

    @admin.action(description='Marcar seleccionados como inactivos')
    def marcar_inactivos(self, request, queryset):
        queryset.update(activo=False)

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('persona', 'matricula', 'programa', 'generacion', 'estado')
    list_filter = ('programa', 'generacion', 'estado')
    search_fields = ('persona__nombres', 'matricula')
