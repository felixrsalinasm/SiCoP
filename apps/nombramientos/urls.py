from django.urls import path
from .views import (
    ListaNombramientos, CrearNombramiento, DetalleNombramiento, EditarNombramiento, EliminarNombramiento,
    ListaTiposNombramiento, CrearTipoNombramiento, EditarTipoNombramiento, EliminarTipoNombramiento,
    AsignarNombramientoProfesor, EliminarNombramientoProfesor,
    AsignarNombramientoPrograma, EliminarNombramientoPrograma,
    VistaExportarNombramientosCSV
)

app_name = 'nombramientos'

urlpatterns = [
    path('', ListaNombramientos.as_view(), name='lista_nombramientos'),
    path('exportar/', VistaExportarNombramientosCSV.as_view(), name='exportar_nombramientos_csv'),
    path('nuevo/', CrearNombramiento.as_view(), name='crear_nombramiento'),
    path('<int:pk>/', DetalleNombramiento.as_view(), name='detalle_nombramiento'),
    path('<int:pk>/editar/', EditarNombramiento.as_view(), name='editar_nombramiento'),
    path('<int:pk>/eliminar/', EliminarNombramiento.as_view(), name='eliminar_nombramiento'),

    path('tipos/', ListaTiposNombramiento.as_view(), name='lista_tipos'),
    path('tipos/nuevo/', CrearTipoNombramiento.as_view(), name='crear_tipo'),
    path('tipos/<int:pk>/editar/', EditarTipoNombramiento.as_view(), name='editar_tipo'),
    path('tipos/<int:pk>/eliminar/', EliminarTipoNombramiento.as_view(), name='eliminar_tipo'),

    path('asignar-profesor/', AsignarNombramientoProfesor.as_view(), name='asignar_profesor'),
    path('asignar-profesor/<int:pk>/eliminar/', EliminarNombramientoProfesor.as_view(), name='eliminar_nombramiento_profesor'),

    path('asignar-programa/', AsignarNombramientoPrograma.as_view(), name='asignar_programa'),
    path('asignar-programa/<int:pk>/eliminar/', EliminarNombramientoPrograma.as_view(), name='eliminar_nombramiento_programa'),
]
