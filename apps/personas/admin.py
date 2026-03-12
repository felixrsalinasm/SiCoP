from django.contrib import admin
from .models import Persona, Profesor, Estudiante

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('paterno', 'materno', 'nombres', 'email', 'genero')
    search_fields = ('paterno', 'materno', 'nombres', 'email', 'rfc', 'curp')
    list_filter = ('genero',)

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('persona', 'grado_academico', 'laboratorio', 'es_externo', 'activo', 'total_alumnos_activos')
    search_fields = ('persona__paterno', 'persona__nombres')
    list_filter = ('grado_academico', 'es_externo', 'activo', 'laboratorio')

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'persona', 'programa', 'generacion', 'modalidad', 'estado')
    search_fields = ('matricula', 'persona__paterno', 'persona__nombres')
    list_filter = ('programa', 'estado', 'modalidad', 'generacion')
