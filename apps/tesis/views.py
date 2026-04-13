from apps.historial.utils import registrar_accion
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import Tesis, DirectorTesis, ComiteTutorial, JuradoExamen
from .forms import FormularioTesis, FormularioDirectorTesis, FormularioComiteTutorial, FormularioJuradoExamen
from apps.cuentas.decoradores import grupo_requerido

GRUPOS_LECTURA = ('Administrador', 'Secretaria', 'Profesor')
GRUPOS_ESCRITURA = ('Administrador', 'Secretaria')
GRUPOS_ADMIN = ('Administrador',)
GRUPOS_TODOS = ('Administrador', 'Coordinador', 'Secretaria', 'Profesor')


@method_decorator(grupo_requerido(*GRUPOS_LECTURA), name='dispatch')
class ListaTesis(ListView):
    model = Tesis
    template_name = 'tesis/lista_tesis.html'
    context_object_name = 'tesis_lista'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('alumno__persona', 'programa')
        estado = self.request.GET.get('estado')
        q = self.request.GET.get('q', '')
        if estado:
            qs = qs.filter(estado=estado)
        if q:
            qs = qs.filter(titulo__icontains=q)
        return qs


@method_decorator(grupo_requerido(*GRUPOS_LECTURA), name='dispatch')
class DetalleTesis(DetailView):
    model = Tesis
    template_name = 'tesis/detalle_tesis.html'
    context_object_name = 'tesis'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['directores'] = self.object.directores.select_related('profesor__persona').filter(activo=True)
        context['comite'] = self.object.comite_tutorial.select_related('profesor__persona').filter(activo=True)
        return context


@method_decorator(grupo_requerido(*GRUPOS_ESCRITURA), name='dispatch')
class CrearTesis(CreateView):
    model = Tesis
    form_class = FormularioTesis
    template_name = 'tesis/form_tesis.html'
    success_url = reverse_lazy('tesis:lista_tesis')

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_accion(self.request, 'CREAR', 'Tesis', f'Crear registro: {self.object}')
        messages.success(self.request, 'Tesis registrada correctamente.')
        return response


@method_decorator(grupo_requerido(*GRUPOS_ESCRITURA), name='dispatch')
class EditarTesis(UpdateView):
    model = Tesis
    form_class = FormularioTesis
    template_name = 'tesis/form_tesis.html'
    success_url = reverse_lazy('tesis:lista_tesis')

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_accion(self.request, 'EDITAR', 'Tesis', f'Editar registro: {self.object}')
        messages.success(self.request, 'Tesis actualizada correctamente.')
        return response


@method_decorator(grupo_requerido(*GRUPOS_ADMIN), name='dispatch')
class EliminarTesis(DeleteView):
    model = Tesis
    template_name = 'tesis/confirmar_eliminar.html'
    success_url = reverse_lazy('tesis:lista_tesis')

    def form_valid(self, form):
        registrar_accion(self.request, 'ELIMINAR', 'Tesis', f'Eliminar registro: {self.object}')
        messages.success(self.request, 'Tesis eliminada correctamente.')
        return super().form_valid(form)


@method_decorator(grupo_requerido(*GRUPOS_LECTURA), name='dispatch')
class ListaDirectoresTesis(ListView):
    model = DirectorTesis
    template_name = 'tesis/lista_directores.html'
    context_object_name = 'directores'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('tesis__alumno__persona', 'profesor__persona', 'tesis__programa')
        estado = self.request.GET.get('estado')
        if estado == 'activo':
            qs = qs.filter(activo=True)
        elif estado == 'inactivo':
            qs = qs.filter(activo=False)
        return qs.order_by('-fecha_asignacion')


@method_decorator(grupo_requerido(*GRUPOS_ESCRITURA), name='dispatch')
class AsignarDirectorTesis(CreateView):
    model = DirectorTesis
    form_class = FormularioDirectorTesis
    template_name = 'tesis/form_director.html'
    success_url = reverse_lazy('tesis:lista_directores')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            registrar_accion(self.request, 'CREAR', 'DirectorTesis', f'Crear registro: {self.object}')
            messages.success(self.request, 'Director asignado correctamente.')
            return response
        except IntegrityError:
            form.add_error(None, 'Este profesor ya dirige esta tesis.')
            return self.form_invalid(form)


@method_decorator(grupo_requerido(*GRUPOS_ESCRITURA), name='dispatch')
class EditarDirectorTesis(UpdateView):
    model = DirectorTesis
    fields = ['tipo_direccion', 'fecha_termino', 'activo']
    template_name = 'tesis/form_director.html'
    success_url = reverse_lazy('tesis:lista_directores')

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_accion(self.request, 'EDITAR', 'DirectorTesis', f'Editar registro: {self.object}')
        messages.success(self.request, 'Director actualizado correctamente.')
        return response


@method_decorator(grupo_requerido(*GRUPOS_ADMIN), name='dispatch')
class EliminarDirectorTesis(DeleteView):
    model = DirectorTesis
    template_name = 'tesis/confirmar_eliminar.html'
    success_url = reverse_lazy('tesis:lista_directores')

    def form_valid(self, form):
        registrar_accion(self.request, 'ELIMINAR', 'DirectorTesis', f'Eliminar registro: {self.object}')
        messages.success(self.request, 'Director eliminado correctamente.')
        return super().form_valid(form)


@method_decorator(grupo_requerido(*GRUPOS_LECTURA), name='dispatch')
class ListaComiteTutorial(ListView):
    model = ComiteTutorial
    template_name = 'tesis/lista_comite.html'
    context_object_name = 'comites'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('tesis__alumno__persona', 'profesor__persona')
        estado = self.request.GET.get('estado')
        if estado == 'activo':
            qs = qs.filter(activo=True)
        elif estado == 'inactivo':
            qs = qs.filter(activo=False)
        return qs.order_by('-fecha_asignacion')


@method_decorator(grupo_requerido(*GRUPOS_ESCRITURA), name='dispatch')
class AsignarComiteTutorial(CreateView):
    model = ComiteTutorial
    form_class = FormularioComiteTutorial
    template_name = 'tesis/form_comite.html'
    success_url = reverse_lazy('tesis:lista_comite')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            registrar_accion(self.request, 'CREAR', 'ComiteTutorial', f'Crear registro: {self.object}')
            messages.success(self.request, 'Miembro de comite asignado correctamente.')
            return response
        except IntegrityError:
            form.add_error(None, 'Este profesor ya es miembro del comite tutorial de esta tesis.')
            return self.form_invalid(form)


@method_decorator(grupo_requerido(*GRUPOS_ESCRITURA), name='dispatch')
class EditarComiteTutorial(UpdateView):
    model = ComiteTutorial
    fields = ['rol', 'fecha_termino', 'activo']
    template_name = 'tesis/form_comite.html'
    success_url = reverse_lazy('tesis:lista_comite')

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_accion(self.request, 'EDITAR', 'ComiteTutorial', f'Editar registro: {self.object}')
        messages.success(self.request, 'Miembro de comite actualizado correctamente.')
        return response


@method_decorator(grupo_requerido(*GRUPOS_ADMIN), name='dispatch')
class EliminarComiteTutorial(DeleteView):
    model = ComiteTutorial
    template_name = 'tesis/confirmar_eliminar.html'
    success_url = reverse_lazy('tesis:lista_comite')

    def form_valid(self, form):
        registrar_accion(self.request, 'ELIMINAR', 'ComiteTutorial', f'Eliminar registro: {self.object}')
        messages.success(self.request, 'Miembro de comite eliminado correctamente.')
        return super().form_valid(form)


@method_decorator(grupo_requerido(*GRUPOS_LECTURA), name='dispatch')
class ListaJuradoExamen(ListView):
    model = JuradoExamen
    template_name = 'tesis/lista_jurado.html'
    context_object_name = 'jurados'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('estudiante__persona', 'profesor__persona')
        tipo_examen = self.request.GET.get('tipo_examen')
        resultado = self.request.GET.get('resultado')
        if tipo_examen:
            qs = qs.filter(tipo_examen=tipo_examen)
        if resultado:
            qs = qs.filter(resultado=resultado)
        return qs.order_by('-fecha_examen', 'estudiante')


@method_decorator(grupo_requerido(*GRUPOS_ESCRITURA), name='dispatch')
class AsignarJuradoExamen(CreateView):
    model = JuradoExamen
    form_class = FormularioJuradoExamen
    template_name = 'tesis/form_jurado.html'
    success_url = reverse_lazy('tesis:lista_jurado')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            registrar_accion(self.request, 'CREAR', 'JuradoExamen', f'Crear registro: {self.object}')
            messages.success(self.request, 'Jurado asignado correctamente.')
            return response
        except IntegrityError:
            form.add_error(None, 'Este profesor ya forma parte de este jurado.')
            return self.form_invalid(form)


@method_decorator(grupo_requerido(*GRUPOS_ESCRITURA), name='dispatch')
class EditarJuradoExamen(UpdateView):
    model = JuradoExamen
    fields = ['rol', 'fecha_examen', 'resultado']
    template_name = 'tesis/form_jurado.html'
    success_url = reverse_lazy('tesis:lista_jurado')

    def form_valid(self, form):
        response = super().form_valid(form)
        registrar_accion(self.request, 'EDITAR', 'JuradoExamen', f'Editar registro: {self.object}')
        messages.success(self.request, 'Jurado actualizado correctamente.')
        return response


@method_decorator(grupo_requerido(*GRUPOS_ADMIN), name='dispatch')
class EliminarJuradoExamen(DeleteView):
    model = JuradoExamen
    template_name = 'tesis/confirmar_eliminar.html'
    success_url = reverse_lazy('tesis:lista_jurado')

    def form_valid(self, form):
        registrar_accion(self.request, 'ELIMINAR', 'JuradoExamen', f'Eliminar registro: {self.object}')
        messages.success(self.request, 'Jurado eliminado correctamente.')
        return super().form_valid(form)


@method_decorator(grupo_requerido(*GRUPOS_ADMIN), name='dispatch')
class RegistrarResultadoExamen(View):
    def get(self, request, pk):
        jurado_ref = get_object_or_404(JuradoExamen, pk=pk)
        grupo = JuradoExamen.objects.filter(estudiante=jurado_ref.estudiante, tipo_examen=jurado_ref.tipo_examen)
        return render(request, 'tesis/form_resultado.html', {'grupo': grupo, 'referencia': jurado_ref})

    def post(self, request, pk):
        jurado_ref = get_object_or_404(JuradoExamen, pk=pk)
        grupo = JuradoExamen.objects.filter(estudiante=jurado_ref.estudiante, tipo_examen=jurado_ref.tipo_examen)
        todos_aprobados = True
        for miembro in grupo:
            resultado_str = request.POST.get(f'resultado_{miembro.pk}')
            if resultado_str in [JuradoExamen.Resultado.APROBADO, JuradoExamen.Resultado.NO_APROBADO, JuradoExamen.Resultado.PENDIENTE]:
                miembro.resultado = resultado_str
                miembro.save()
            if miembro.resultado != JuradoExamen.Resultado.APROBADO:
                todos_aprobados = False
        if todos_aprobados:
            estudiante = jurado_ref.estudiante
            if estudiante.estado == 'ACTIVO':
                estudiante.estado = 'EGRESADO'
                estudiante.save()
                messages.success(request, 'Todos aprobaron. Estado del alumno cambiado a EGRESADO.')
        else:
            messages.info(request, 'Los resultados del jurado han sido guardados.')
        return redirect('tesis:lista_jurado')


@method_decorator(grupo_requerido(*GRUPOS_TODOS), name='dispatch')
class VistaEstudiantesDelProfesor(ListView):
    template_name = 'tesis/mis_estudiantes.html'
    context_object_name = 'directores'
    paginate_by = 20

    def get_queryset(self):
        usuario = self.request.user
        qs = DirectorTesis.objects.select_related(
            'tesis__alumno__persona', 'tesis__programa', 'profesor__persona'
        ).filter(activo=True)
        if usuario.groups.filter(name='Profesor').exists() and not usuario.groups.filter(
            name__in=['Administrador', 'Coordinador', 'Secretaria']
        ).exists():
            if hasattr(usuario, 'persona') and hasattr(usuario.persona, 'profesor'):
                qs = qs.filter(profesor=usuario.persona.profesor)
            else:
                qs = qs.none()
        return qs.order_by('-fecha_asignacion')
