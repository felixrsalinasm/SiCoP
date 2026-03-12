from django.contrib import admin
from .models import DirectorTesis, ComiteTutorial, JuradoExamen

@admin.register(DirectorTesis)
class DirectorTesisAdmin(admin.ModelAdmin):
    list_display = ('profesor', 'estudiante', 'es_codirector', 'fecha_asignacion', 'activo')
    list_filter = ('es_codirector', 'activo')
    search_fields = ('profesor__persona__paterno', 'estudiante__matricula')

@admin.register(ComiteTutorial)
class ComiteTutorialAdmin(admin.ModelAdmin):
    list_display = ('profesor', 'estudiante', 'fecha_asignacion', 'activo')
    list_filter = ('activo',)
    search_fields = ('profesor__persona__paterno', 'estudiante__matricula')

@admin.register(JuradoExamen)
class JuradoExamenAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'profesor', 'tipo_examen', 'rol', 'fecha_examen', 'resultado')
    list_filter = ('tipo_examen', 'rol', 'resultado')
