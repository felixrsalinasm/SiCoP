from django.urls import path
from .views import (
    ListaPersonas, DetallePersona, CrearPersona, EditarPersona, EliminarPersona,
    ListaProfesores, CrearProfesor, EditarProfesor, DetalleProfesor, VistaExportarProfesoresCSV,
    ListaEstudiantes, CrearEstudiante, EditarEstudiante, DetalleEstudiante, VistaExportarEstudiantesCSV
)

app_name = 'personas'

urlpatterns = [
    path('', ListaPersonas.as_view(), name='lista_personas'),
    path('nueva/', CrearPersona.as_view(), name='crear_persona'),
    path('<int:pk>/', DetallePersona.as_view(), name='detalle_persona'),
    path('<int:pk>/editar/', EditarPersona.as_view(), name='editar_persona'),
    path('<int:pk>/eliminar/', EliminarPersona.as_view(), name='eliminar_persona'),
    
    path('profesores/', ListaProfesores.as_view(), name='lista_profesores'),
    path('profesores/nuevo/', CrearProfesor.as_view(), name='crear_profesor'),
    path('profesores/exportar/', VistaExportarProfesoresCSV.as_view(), name='exportar_profesores_csv'),
    path('profesores/<int:pk>/', DetalleProfesor.as_view(), name='detalle_profesor'),
    path('profesores/<int:pk>/editar/', EditarProfesor.as_view(), name='editar_profesor'),
    
    path('estudiantes/', ListaEstudiantes.as_view(), name='lista_estudiantes'),
    path('estudiantes/nuevo/', CrearEstudiante.as_view(), name='crear_estudiante'),
    path('estudiantes/exportar/', VistaExportarEstudiantesCSV.as_view(), name='exportar_estudiantes_csv'),
    path('estudiantes/<int:pk>/', DetalleEstudiante.as_view(), name='detalle_estudiante'),
    path('estudiantes/<int:pk>/editar/', EditarEstudiante.as_view(), name='editar_estudiante'),
]
