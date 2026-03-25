from django.urls import path
from .views import (
    ListaTesis, DetalleTesis, CrearTesis, EditarTesis, EliminarTesis,
    ListaDirectoresTesis, AsignarDirectorTesis, EditarDirectorTesis, EliminarDirectorTesis,
    ListaComiteTutorial, AsignarComiteTutorial, EditarComiteTutorial, EliminarComiteTutorial,
    ListaJuradoExamen, AsignarJuradoExamen, EditarJuradoExamen, RegistrarResultadoExamen
)

app_name = 'tesis'

urlpatterns = [
    path('', ListaTesis.as_view(), name='lista_tesis'),
    path('<int:pk>/', DetalleTesis.as_view(), name='detalle_tesis'),
    path('crear/', CrearTesis.as_view(), name='crear_tesis'),
    path('<int:pk>/editar/', EditarTesis.as_view(), name='editar_tesis'),
    path('<int:pk>/eliminar/', EliminarTesis.as_view(), name='eliminar_tesis'),

    path('directores/', ListaDirectoresTesis.as_view(), name='lista_directores'),
    path('directores/asignar/', AsignarDirectorTesis.as_view(), name='asignar_director'),
    path('directores/<int:pk>/editar/', EditarDirectorTesis.as_view(), name='editar_director'),
    path('directores/<int:pk>/eliminar/', EliminarDirectorTesis.as_view(), name='eliminar_director'),

    path('comite/', ListaComiteTutorial.as_view(), name='lista_comite'),
    path('comite/asignar/', AsignarComiteTutorial.as_view(), name='asignar_comite'),
    path('comite/<int:pk>/editar/', EditarComiteTutorial.as_view(), name='editar_comite'),
    path('comite/<int:pk>/eliminar/', EliminarComiteTutorial.as_view(), name='eliminar_comite'),

    path('jurado/', ListaJuradoExamen.as_view(), name='lista_jurado'),
    path('jurado/asignar/', AsignarJuradoExamen.as_view(), name='asignar_jurado'),
    path('jurado/<int:pk>/editar/', EditarJuradoExamen.as_view(), name='editar_jurado'),
    path('jurado/<int:pk>/resultado/', RegistrarResultadoExamen.as_view(), name='resultado_jurado'),
]
