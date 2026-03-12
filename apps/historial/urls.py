from django.urls import path
from .views import VistaListaRegistros

app_name = 'historial'

urlpatterns = [
    path('', VistaListaRegistros.as_view(), name='historial_lista'),
]
