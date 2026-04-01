from apps.historial.utils import registrar_accion
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.http import HttpResponse
import csv
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib import messages
from .models import Persona, Profesor, Estudiante
from .forms import FormularioPersona, FormularioProfesor, FormularioEstudiante
from apps.cuentas.decoradores import grupo_requerido

GRUPOS_LECTURA = ('Administrador', 'Secretaria')
GRUPOS_ESCRITURA = ('Administrador', 'Secretaria')
GRUPOS_ADMIN = ('Administrador',)
GRUPOS_PROFESOR_VER = ('Administrador', 'Secretaria', 'Profesor')


@method_decorator(grupo_requerido(*GRUPOS_LECTURA), name='dispatch')
class ListaPersonas(ListView):
    model = Persona
    template_name = 'personas/lista_personas.html'
    context_object_name = 'personas'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(nombres__icontains=query) |
                Q(paterno__icontains=query) |
                Q(email__icontains=query)
            )
        return qs


@method_decorator(grupo_requerido(*GRUPOS_LECTURA), name='dispatch')
class DetallePersona(DetailView):
    model = Persona
    template_name = 'personas/detalle_persona.html'
    context_object_name = 'persona'


@method_decorator(grupo_requerido(*GRUPOS_ESCRITURA), name='dispatch')
class CrearPersona(CreateView):
    model = Persona
    form_class = FormularioPersona
    template_name = 'personas/form_persona.html'
    success_url = reverse_lazy('personas:lista_personas')

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_accion(self.request, 'CREAR', 'Persona', f'Crear registro: {self.object}')
        messages.success(self.request, 'Persona registrada correctamente.')
        return response


@method_decorator(grupo_requerido(*GRUPOS_ESCRITURA), name='dispatch')
class EditarPersona(UpdateView):
    model = Persona
    form_class = FormularioPersona
    template_name = 'personas/form_persona.html'
    success_url = reverse_lazy('personas:lista_personas')

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_accion(self.request, 'EDITAR', 'Persona', f'Editar registro: {self.object}')
        messages.success(self.request, 'Persona actualizada correctamente.')
        return response


@method_decorator(grupo_requerido(*GRUPOS_ADMIN), name='dispatch')
class EliminarPersona(DeleteView):
    model = Persona
    template_name = 'personas/confirmar_eliminar.html'
    success_url = reverse_lazy('personas:lista_personas')

    def form_valid(self, form):
        registrar_accion(self.request, 'ELIMINAR', 'Persona', f'Eliminar registro: {self.object}')
        messages.success(self.request, 'Persona eliminada correctamente.')
        return super().form_valid(form)


@method_decorator(grupo_requerido(*GRUPOS_LECTURA), name='dispatch')
class ListaProfesores(ListView):
    model = Profesor
    template_name = 'personas/lista_profesores.html'
    context_object_name = 'profesores'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(persona__nombres__icontains=query) |
                Q(persona__paterno__icontains=query)
            )
        return qs


@method_decorator(grupo_requerido(*GRUPOS_ESCRITURA), name='dispatch')
class CrearProfesor(View):
    def get(self, request):
        email = request.GET.get('email', '')
        persona = Persona.objects.filter(email=email).first() if email else None
        form_persona = FormularioPersona(instance=persona)
        form_profesor = FormularioProfesor()
        if persona:
            for field in form_persona.fields.values():
                field.widget.attrs['readonly'] = True
        return render(request, 'personas/form_profesor.html', {
            'form_persona': form_persona,
            'form_profesor': form_profesor,
            'persona': persona,
            'email_busqueda': email
        })

    def post(self, request):
        email = request.POST.get('email_busqueda')
        persona = Persona.objects.filter(email=email).first() if email else None
        form_persona = FormularioPersona(request.POST, request.FILES, instance=persona)
        form_profesor = FormularioProfesor(request.POST)
        if persona:
            if form_profesor.is_valid():
                profesor = form_profesor.save(commit=False)
                profesor.persona = persona
                profesor.save()
                messages.success(request, 'Profesor registrado correctamente.')
                return redirect('personas:lista_profesores')
        else:
            if form_persona.is_valid() and form_profesor.is_valid():
                persona_nueva = form_persona.save()
                profesor = form_profesor.save(commit=False)
                profesor.persona = persona_nueva
                profesor.save()
                messages.success(request, 'Profesor registrado correctamente.')
                return redirect('personas:lista_profesores')
        return render(request, 'personas/form_profesor.html', {
            'form_persona': form_persona,
            'form_profesor': form_profesor,
            'persona': persona,
            'email_busqueda': email
        })


@method_decorator(grupo_requerido(*GRUPOS_ESCRITURA), name='dispatch')
class EditarProfesor(View):
    def get(self, request, pk):
        profesor = get_object_or_404(Profesor, pk=pk)
        form_persona = FormularioPersona(instance=profesor.persona)
        form_profesor = FormularioProfesor(instance=profesor)
        return render(request, 'personas/form_profesor.html', {
            'form_persona': form_persona,
            'form_profesor': form_profesor,
            'es_edicion': True
        })

    def post(self, request, pk):
        profesor = get_object_or_404(Profesor, pk=pk)
        form_persona = FormularioPersona(request.POST, request.FILES, instance=profesor.persona)
        form_profesor = FormularioProfesor(request.POST, instance=profesor)
        if form_persona.is_valid() and form_profesor.is_valid():
            form_persona.save()
            form_profesor.save()
            messages.success(request, 'Profesor actualizado correctamente.')
            return redirect('personas:lista_profesores')
        return render(request, 'personas/form_profesor.html', {
            'form_persona': form_persona,
            'form_profesor': form_profesor,
            'es_edicion': True
        })


@method_decorator(grupo_requerido(*GRUPOS_PROFESOR_VER), name='dispatch')
class DetalleProfesor(DetailView):
    model = Profesor
    template_name = 'personas/detalle_profesor.html'
    context_object_name = 'profesor'


@method_decorator(grupo_requerido(*GRUPOS_LECTURA), name='dispatch')
class ListaEstudiantes(ListView):
    model = Estudiante
    template_name = 'personas/lista_estudiantes.html'
    context_object_name = 'estudiantes'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        programa = self.request.GET.get('programa')
        estado = self.request.GET.get('estado')
        if query:
            qs = qs.filter(
                Q(persona__nombres__icontains=query) |
                Q(persona__paterno__icontains=query) |
                Q(matricula__icontains=query)
            )
        if programa:
            qs = qs.filter(programa_id=programa)
        if estado:
            qs = qs.filter(estado=estado)
        return qs

    def get_context_data(self, **kwargs):
        from apps.programas.models import Programa
        context = super().get_context_data(**kwargs)
        context['programas'] = Programa.objects.filter(activo=True)
        context['estados'] = Estudiante.Estado.choices
        return context


@method_decorator(grupo_requerido(*GRUPOS_ESCRITURA), name='dispatch')
class CrearEstudiante(View):
    def get(self, request):
        email = request.GET.get('email', '')
        persona = Persona.objects.filter(email=email).first() if email else None
        form_persona = FormularioPersona(instance=persona)
        form_estudiante = FormularioEstudiante()
        if persona:
            for field in form_persona.fields.values():
                field.widget.attrs['readonly'] = True
        return render(request, 'personas/form_estudiante.html', {
            'form_persona': form_persona,
            'form_estudiante': form_estudiante,
            'persona': persona,
            'email_busqueda': email
        })

    def post(self, request):
        email = request.POST.get('email_busqueda')
        persona = Persona.objects.filter(email=email).first() if email else None
        form_persona = FormularioPersona(request.POST, request.FILES, instance=persona)
        form_estudiante = FormularioEstudiante(request.POST)
        if persona:
            if form_estudiante.is_valid():
                estudiante = form_estudiante.save(commit=False)
                estudiante.persona = persona
                estudiante.save()
                messages.success(request, 'Alumno registrado correctamente.')
                return redirect('personas:lista_estudiantes')
        else:
            if form_persona.is_valid() and form_estudiante.is_valid():
                persona_nueva = form_persona.save()
                estudiante = form_estudiante.save(commit=False)
                estudiante.persona = persona_nueva
                estudiante.save()
                messages.success(request, 'Alumno registrado correctamente.')
                return redirect('personas:lista_estudiantes')
        return render(request, 'personas/form_estudiante.html', {
            'form_persona': form_persona,
            'form_estudiante': form_estudiante,
            'persona': persona,
            'email_busqueda': email
        })


@method_decorator(grupo_requerido(*GRUPOS_ESCRITURA), name='dispatch')
class EditarEstudiante(View):
    def get(self, request, pk):
        estudiante = get_object_or_404(Estudiante, pk=pk)
        form_persona = FormularioPersona(instance=estudiante.persona)
        form_estudiante = FormularioEstudiante(instance=estudiante)
        return render(request, 'personas/form_estudiante.html', {
            'form_persona': form_persona,
            'form_estudiante': form_estudiante,
            'es_edicion': True
        })

    def post(self, request, pk):
        estudiante = get_object_or_404(Estudiante, pk=pk)
        form_persona = FormularioPersona(request.POST, request.FILES, instance=estudiante.persona)
        form_estudiante = FormularioEstudiante(request.POST, instance=estudiante)
        if form_persona.is_valid() and form_estudiante.is_valid():
            form_persona.save()
            form_estudiante.save()
            messages.success(request, 'Alumno actualizado correctamente.')
            return redirect('personas:lista_estudiantes')
        return render(request, 'personas/form_estudiante.html', {
            'form_persona': form_persona,
            'form_estudiante': form_estudiante,
            'es_edicion': True
        })


@method_decorator(grupo_requerido(*GRUPOS_LECTURA), name='dispatch')
class DetalleEstudiante(DetailView):
    model = Estudiante
    template_name = 'personas/detalle_estudiante.html'
    context_object_name = 'estudiante'


@method_decorator(grupo_requerido(*GRUPOS_LECTURA), name='dispatch')
class VistaExportarProfesoresCSV(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="profesores_CIC.csv"'
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        writer.writerow(['Nombre Completo', 'Grado', 'Laboratorio', 'Correo', 'Activo'])
        for prof in Profesor.objects.select_related('persona', 'laboratorio').all():
            writer.writerow([
                prof.persona.nombre_completo,
                prof.get_grado_academico_display(),
                prof.laboratorio.nombre if prof.laboratorio else '-',
                prof.persona.email,
                'Si' if prof.activo else 'No'
            ])
        return response


@method_decorator(grupo_requerido(*GRUPOS_LECTURA), name='dispatch')
class VistaExportarEstudiantesCSV(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="estudiantes_CIC.csv"'
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        writer.writerow(['Nombre Completo', 'Matricula', 'Programa', 'Generacion', 'Modalidad', 'Estado', 'Correo'])
        for est in Estudiante.objects.select_related('persona', 'programa').all():
            writer.writerow([
                est.persona.nombre_completo,
                est.matricula,
                est.programa.siglas,
                est.generacion,
                est.get_modalidad_display(),
                est.get_estado_display(),
                est.persona.email
            ])
        return response
