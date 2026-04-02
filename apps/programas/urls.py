from django.urls import path
from .views import (
    ListaLaboratorios, CrearLaboratorio, EditarLaboratorio, DetalleLaboratorio, EliminarLaboratorio,
    ListaProgramas, CrearPrograma, EditarPrograma, DetallePrograma, EliminarPrograma,
    ListaCoordinadores, AsignarCoordinador, EditarCoordinador, EliminarCoordinador
)

app_name = 'programas'

urlpatterns = [
    path('laboratorios/', ListaLaboratorios.as_view(), name='lista_laboratorios'),
    path('laboratorios/nuevo/', CrearLaboratorio.as_view(), name='crear_laboratorio'),
    path('laboratorios/<int:pk>/', DetalleLaboratorio.as_view(), name='detalle_laboratorio'),
    path('laboratorios/<int:pk>/editar/', EditarLaboratorio.as_view(), name='editar_laboratorio'),
    path('laboratorios/<int:pk>/eliminar/', EliminarLaboratorio.as_view(), name='eliminar_laboratorio'),

    path('programas/', ListaProgramas.as_view(), name='lista_programas'),
    path('programas/nuevo/', CrearPrograma.as_view(), name='crear_programa'),
    path('programas/<int:pk>/', DetallePrograma.as_view(), name='detalle_programa'),
    path('programas/<int:pk>/editar/', EditarPrograma.as_view(), name='editar_programa'),
    path('programas/<int:pk>/eliminar/', EliminarPrograma.as_view(), name='eliminar_programa'),

    path('coordinadores/', ListaCoordinadores.as_view(), name='lista_coordinadores'),
    path('coordinadores/asignar/', AsignarCoordinador.as_view(), name='asignar_coordinador'),
    path('coordinadores/<int:pk>/editar/', EditarCoordinador.as_view(), name='editar_coordinador'),
    path('coordinadores/<int:pk>/eliminar/', EliminarCoordinador.as_view(), name='eliminar_coordinador'),
]
