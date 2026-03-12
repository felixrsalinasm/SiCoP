from django.contrib import admin
from .models import CatTipoNombramiento, Nombramiento, NombramientoProfesor, ProgramaNombramiento

@admin.register(CatTipoNombramiento)
class CatTipoNombramientoAdmin(admin.ModelAdmin):
    list_display = ('nombramiento', 'origen')
    list_filter = ('origen',)

@admin.register(Nombramiento)
class NombramientoAdmin(admin.ModelAdmin):
    list_display = ('clave', 'tipo', 'fecha_emision', 'fecha_vencimiento', 'esta_vigente')
    list_filter = ('tipo__origen',)
    search_fields = ('clave',)

@admin.register(NombramientoProfesor)
class NombramientoProfesorAdmin(admin.ModelAdmin):
    list_display = ('profesor', 'nombramiento')
    search_fields = ('profesor__persona__paterno',)

@admin.register(ProgramaNombramiento)
class ProgramaNombramientoAdmin(admin.ModelAdmin):
    list_display = ('programa', 'nombramiento')
