from django.contrib import admin
from .models import DirectorTesis, ComiteTutorial, JuradoExamen

@admin.register(DirectorTesis)
class DirectorTesisAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'profesor', 'activo')
    list_filter = ('activo',)

@admin.register(ComiteTutorial)
class ComiteTutorialAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'profesor')
    list_filter = ('activo',)

@admin.register(JuradoExamen)
class JuradoExamenAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'profesor', 'resultado')
    list_filter = ('resultado',)
