from django.urls import path
from .views import (
    ListaDirectoresTesis, AsignarDirectorTesis, EditarDirectorTesis, DesactivarDirectorTesis,
    ListaComiteTutorial, AsignarComiteTutorial, EditarComiteTutorial,
    ListaJuradoExamen, AsignarJuradoExamen, EditarJuradoExamen, RegistrarResultadoExamen
)

app_name = 'tesis'

urlpatterns = [
    path('directores/', ListaDirectoresTesis.as_view(), name='lista_directores'),
    path('directores/asignar/', AsignarDirectorTesis.as_view(), name='asignar_director'),
    path('directores/<int:pk>/editar/', EditarDirectorTesis.as_view(), name='editar_director'),
    path('directores/<int:pk>/desactivar/', DesactivarDirectorTesis.as_view(), name='desactivar_director'),
    
    path('comite/', ListaComiteTutorial.as_view(), name='lista_comite'),
    path('comite/asignar/', AsignarComiteTutorial.as_view(), name='asignar_comite'),
    path('comite/<int:pk>/editar/', EditarComiteTutorial.as_view(), name='editar_comite'),
    
    path('jurado/', ListaJuradoExamen.as_view(), name='lista_jurado'),
    path('jurado/asignar/', AsignarJuradoExamen.as_view(), name='asignar_jurado'),
    path('jurado/<int:pk>/editar/', EditarJuradoExamen.as_view(), name='editar_jurado'),
    path('jurado/<int:pk>/resultado/', RegistrarResultadoExamen.as_view(), name='resultado_jurado'),
]
