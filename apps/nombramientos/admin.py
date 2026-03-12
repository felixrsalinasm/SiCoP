from django.contrib import admin
from .models import CatTipoNombramiento, Nombramiento, NombramientoProfesor, ProgramaNombramiento

@admin.register(CatTipoNombramiento)
class CatTipoNombramientoAdmin(admin.ModelAdmin):
    list_display = ('nombramiento', 'origen')
    search_fields = ('nombramiento', 'origen')

@admin.register(Nombramiento)
class NombramientoAdmin(admin.ModelAdmin):
    list_display = ('obtener_profesor', 'tipo', 'clave', 'fecha_emision', 'fecha_vencimiento')
    list_filter = ('tipo',)
    search_fields = ('profesores_nombramiento__profesor__persona__nombres', 'clave')
    readonly_fields = ('fecha_emision',)

    @admin.display(description='Profesor')
    def obtener_profesor(self, obj):
        rel = obj.profesores_nombramiento.first()
        return rel.profesor if rel else '-'
