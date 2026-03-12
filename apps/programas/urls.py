from django.urls import path
from .views import (
    ListaLaboratorios, CrearLaboratorio, EditarLaboratorio, DetalleLaboratorio,
    ListaProgramas, CrearPrograma, EditarPrograma, DetallePrograma,
    ListaCoordinadores, AsignarCoordinador, EditarCoordinador
)

app_name = 'programas'

urlpatterns = [
    path('laboratorios/', ListaLaboratorios.as_view(), name='lista_laboratorios'),
    path('laboratorios/nuevo/', CrearLaboratorio.as_view(), name='crear_laboratorio'),
    path('laboratorios/<int:pk>/', DetalleLaboratorio.as_view(), name='detalle_laboratorio'),
    path('laboratorios/<int:pk>/editar/', EditarLaboratorio.as_view(), name='editar_laboratorio'),
    
    path('programas/', ListaProgramas.as_view(), name='lista_programas'),
    path('programas/nuevo/', CrearPrograma.as_view(), name='crear_programa'),
    path('programas/<int:pk>/', DetallePrograma.as_view(), name='detalle_programa'),
    path('programas/<int:pk>/editar/', EditarPrograma.as_view(), name='editar_programa'),
    
    path('coordinadores/', ListaCoordinadores.as_view(), name='lista_coordinadores'),
    path('coordinadores/asignar/', AsignarCoordinador.as_view(), name='asignar_coordinador'),
    path('coordinadores/<int:pk>/editar/', EditarCoordinador.as_view(), name='editar_coordinador'),
]
