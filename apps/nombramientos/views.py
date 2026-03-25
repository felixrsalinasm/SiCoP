from apps.historial.utils import registrar_accion
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.http import HttpResponse
import csv
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.utils import timezone
from .models import CatTipoNombramiento, Nombramiento, NombramientoProfesor, ProgramaNombramiento
from .forms import FormularioTipoNombramiento, FormularioNombramiento, FormularioNombramientoProfesor, FormularioNombramientoPrograma
from apps.cuentas.decoradores import rol_requerido
from django.db import IntegrityError
from django.contrib import messages

ROLES_TODO = ['ADMIN', 'COORDINADOR', 'SECRETARIA']
ROLES_ESCRITURA = ['ADMIN', 'SECRETARIA']
ROLES_ADMIN = ['ADMIN']
ROLES_ADMIN_COORD = ['ADMIN', 'COORDINADOR']

@method_decorator(rol_requerido(*ROLES_ADMIN_COORD), name='dispatch')
class ListaTiposNombramiento(ListView):
    model = CatTipoNombramiento
    paginate_by = 20
    template_name = 'nombramientos/lista_tipos.html'
    context_object_name = 'tipos'

@method_decorator(rol_requerido(*ROLES_ADMIN_COORD), name='dispatch')
class CrearTipoNombramiento(CreateView):
    model = CatTipoNombramiento
    form_class = FormularioTipoNombramiento
    template_name = 'nombramientos/form_tipo.html'
    success_url = reverse_lazy('nombramientos:lista_tipos')


    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_accion(self.request, 'CREAR', 'TipoNombramiento', f'Crear registro: {self.object}')
        return response

@method_decorator(rol_requerido(*ROLES_ADMIN_COORD), name='dispatch')
class EditarTipoNombramiento(UpdateView):
    model = CatTipoNombramiento
    form_class = FormularioTipoNombramiento
    template_name = 'nombramientos/form_tipo.html'
    success_url = reverse_lazy('nombramientos:lista_tipos')


    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_accion(self.request, 'EDITAR', 'TipoNombramiento', f'Editar registro: {self.object}')
        return response

@method_decorator(rol_requerido(*ROLES_TODO), name='dispatch')
class ListaNombramientos(ListView):
    model = Nombramiento
    template_name = 'nombramientos/lista_nombramientos.html'
    context_object_name = 'nombramientos'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        origen = self.request.GET.get('origen')
        estado = self.request.GET.get('estado')
        
        if origen:
            qs = qs.filter(tipo__origen=origen)
        
        if estado == 'vigente':
            qs = qs.filter(fecha_vencimiento__gte=timezone.now().date())
        elif estado == 'vencido':
            qs = qs.filter(fecha_vencimiento__lt=timezone.now().date())
            
        return qs

@method_decorator(rol_requerido(*ROLES_TODO), name='dispatch')
class DetalleNombramiento(DetailView):
    model = Nombramiento
    template_name = 'nombramientos/detalle_nombramiento.html'
    context_object_name = 'nombramiento'

@method_decorator(rol_requerido(*ROLES_ADMIN_COORD), name='dispatch')
class VistaExportarNombramientosCSV(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="nombramientos_CIC.csv"'
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        writer.writerow(['Profesor', 'Tipo', 'Institucion', 'Clave', 'Fecha Emision', 'Fecha Vencimiento'])
        for nom in Nombramiento.objects.select_related('tipo').all():
            rel = nom.profesores_nombramiento.first()
            prof_nombre = rel.profesor.persona.nombre_completo if rel else '-'
            writer.writerow([
                prof_nombre,
                nom.tipo.nombramiento,
                nom.tipo.get_origen_display(),
                nom.clave,
                nom.fecha_emision,
                nom.fecha_vencimiento
            ])
        return response

@method_decorator(rol_requerido(*ROLES_ESCRITURA), name='dispatch')
class CrearNombramiento(CreateView):
    model = Nombramiento
    form_class = FormularioNombramiento
    template_name = 'nombramientos/form_nombramiento.html'
    success_url = reverse_lazy('nombramientos:lista_nombramientos')


    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_accion(self.request, 'CREAR', 'Nombramiento', f'Crear registro: {self.object}')
        return response

@method_decorator(rol_requerido(*ROLES_ESCRITURA), name='dispatch')
class EditarNombramiento(UpdateView):
    model = Nombramiento
    form_class = FormularioNombramiento
    template_name = 'nombramientos/form_nombramiento.html'
    success_url = reverse_lazy('nombramientos:lista_nombramientos')


    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_accion(self.request, 'EDITAR', 'Nombramiento', f'Editar registro: {self.object}')
        return response

@method_decorator(rol_requerido(*ROLES_ADMIN), name='dispatch')
class EliminarNombramiento(DeleteView):
    model = Nombramiento
    template_name = 'nombramientos/confirmar_eliminar.html'
    success_url = reverse_lazy('nombramientos:lista_nombramientos')


    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        registrar_accion(self.request, 'ELIMINAR', 'Nombramiento', f'Eliminar registro: {obj}')
        return super().delete(request, *args, **kwargs)

@method_decorator(rol_requerido(*ROLES_ESCRITURA), name='dispatch')
class AsignarNombramientoProfesor(CreateView):
    model = NombramientoProfesor
    form_class = FormularioNombramientoProfesor
    template_name = 'nombramientos/form_asignar_profesor.html'
    
    def get_success_url(self):
        return reverse_lazy('nombramientos:detalle_nombramiento', kwargs={'pk': self.object.nombramiento.pk})

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            registrar_accion(self.request, 'CREAR', 'NombramientoProfesor', f'Crear registro: {self.object}')
            return response
        except IntegrityError:
            form.add_error(None, 'Este profesor ya tiene asignado este nombramiento.')
            return self.form_invalid(form)

@method_decorator(rol_requerido(*ROLES_ADMIN), name='dispatch')
class EliminarNombramientoProfesor(DeleteView):
    model = NombramientoProfesor
    template_name = 'nombramientos/confirmar_eliminar.html'
    
    def get_success_url(self):
        return reverse_lazy('nombramientos:detalle_nombramiento', kwargs={'pk': self.object.nombramiento.pk})


    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        registrar_accion(self.request, 'ELIMINAR', 'NombramientoProfesor', f'Eliminar registro: {obj}')
        return super().delete(request, *args, **kwargs)

@method_decorator(rol_requerido(*ROLES_ADMIN), name='dispatch')
class AsignarNombramientoPrograma(CreateView):
    model = ProgramaNombramiento
    form_class = FormularioNombramientoPrograma
    template_name = 'nombramientos/form_asignar_programa.html'
    
    def get_success_url(self):
        return reverse_lazy('nombramientos:detalle_nombramiento', kwargs={'pk': self.object.nombramiento.pk})

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            registrar_accion(self.request, 'CREAR', 'NombramientoPrograma', f'Crear registro: {self.object}')
            return response
        except IntegrityError:
            form.add_error(None, 'Este programa ya tiene asignado este nombramiento.')
            return self.form_invalid(form)

@method_decorator(rol_requerido(*ROLES_ADMIN), name='dispatch')
class EliminarNombramientoPrograma(DeleteView):
    model = ProgramaNombramiento
    template_name = 'nombramientos/confirmar_eliminar.html'
    
    def get_success_url(self):
        return reverse_lazy('nombramientos:detalle_nombramiento', kwargs={'pk': self.object.nombramiento.pk})


    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        registrar_accion(self.request, 'ELIMINAR', 'NombramientoPrograma', f'Eliminar registro: {obj}')
        return super().delete(request, *args, **kwargs)
