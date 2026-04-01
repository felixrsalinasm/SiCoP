from apps.historial.utils import registrar_accion
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib import messages
from .models import Laboratorio, Programa, Coordinador
from .forms import FormularioLaboratorio, FormularioPrograma, FormularioCoordinador
from apps.cuentas.decoradores import grupo_requerido

GRUPOS_LECTURA = ('Administrador', 'Secretaria')
GRUPOS_ADMIN = ('Administrador',)


@method_decorator(grupo_requerido(*GRUPOS_ADMIN), name='dispatch')
class ListaLaboratorios(ListView):
    model = Laboratorio
    paginate_by = 20
    template_name = 'programas/lista_laboratorios.html'
    context_object_name = 'laboratorios'


@method_decorator(grupo_requerido(*GRUPOS_ADMIN), name='dispatch')
class CrearLaboratorio(CreateView):
    model = Laboratorio
    form_class = FormularioLaboratorio
    template_name = 'programas/form_laboratorio.html'
    success_url = reverse_lazy('programas:lista_laboratorios')

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_accion(self.request, 'CREAR', 'Laboratorio', f'Crear registro: {self.object}')
        messages.success(self.request, 'Laboratorio creado correctamente.')
        return response


@method_decorator(grupo_requerido(*GRUPOS_ADMIN), name='dispatch')
class EditarLaboratorio(UpdateView):
    model = Laboratorio
    form_class = FormularioLaboratorio
    template_name = 'programas/form_laboratorio.html'
    success_url = reverse_lazy('programas:lista_laboratorios')

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_accion(self.request, 'EDITAR', 'Laboratorio', f'Editar registro: {self.object}')
        messages.success(self.request, 'Laboratorio actualizado correctamente.')
        return response


@method_decorator(grupo_requerido(*GRUPOS_ADMIN), name='dispatch')
class DetalleLaboratorio(DetailView):
    model = Laboratorio
    template_name = 'programas/detalle_laboratorio.html'
    context_object_name = 'laboratorio'


@method_decorator(grupo_requerido(*GRUPOS_ADMIN), name='dispatch')
class ListaProgramas(ListView):
    model = Programa
    paginate_by = 20
    template_name = 'programas/lista_programas.html'
    context_object_name = 'programas'


@method_decorator(grupo_requerido(*GRUPOS_ADMIN), name='dispatch')
class DetallePrograma(DetailView):
    model = Programa
    template_name = 'programas/detalle_programa.html'
    context_object_name = 'programa'


@method_decorator(grupo_requerido(*GRUPOS_ADMIN), name='dispatch')
class CrearPrograma(CreateView):
    model = Programa
    form_class = FormularioPrograma
    template_name = 'programas/form_programa.html'
    success_url = reverse_lazy('programas:lista_programas')

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_accion(self.request, 'CREAR', 'Programa', f'Crear registro: {self.object}')
        messages.success(self.request, 'Programa creado correctamente.')
        return response


@method_decorator(grupo_requerido(*GRUPOS_ADMIN), name='dispatch')
class EditarPrograma(UpdateView):
    model = Programa
    form_class = FormularioPrograma
    template_name = 'programas/form_programa.html'
    success_url = reverse_lazy('programas:lista_programas')

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_accion(self.request, 'EDITAR', 'Programa', f'Editar registro: {self.object}')
        messages.success(self.request, 'Programa actualizado correctamente.')
        return response


@method_decorator(grupo_requerido(*GRUPOS_ADMIN), name='dispatch')
class ListaCoordinadores(ListView):
    model = Coordinador
    paginate_by = 20
    template_name = 'programas/lista_coordinadores.html'
    context_object_name = 'coordinadores'

    def get_queryset(self):
        return super().get_queryset().order_by('programa', '-fecha_inicio')


@method_decorator(grupo_requerido(*GRUPOS_ADMIN), name='dispatch')
class AsignarCoordinador(CreateView):
    model = Coordinador
    form_class = FormularioCoordinador
    template_name = 'programas/form_coordinador.html'
    success_url = reverse_lazy('programas:lista_coordinadores')

    def form_valid(self, form):
        programa = form.cleaned_data['programa']
        coordinador_actual = Coordinador.objects.filter(programa=programa, fecha_fin__isnull=True).first()
        if coordinador_actual:
            coordinador_actual.fecha_fin = timezone.now().date()
            coordinador_actual.save()
        response = super().form_valid(form)
        registrar_accion(self.request, 'CREAR', 'Coordinador', f'Crear registro: {self.object}')
        messages.success(self.request, 'Coordinador asignado correctamente.')
        return response


@method_decorator(grupo_requerido(*GRUPOS_ADMIN), name='dispatch')
class EditarCoordinador(UpdateView):
    model = Coordinador
    form_class = FormularioCoordinador
    template_name = 'programas/form_coordinador.html'
    success_url = reverse_lazy('programas:lista_coordinadores')

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_accion(self.request, 'EDITAR', 'Coordinador', f'Editar registro: {self.object}')
        messages.success(self.request, 'Coordinador actualizado correctamente.')
        return response
