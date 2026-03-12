from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, View
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils import timezone
from .models import DirectorTesis, ComiteTutorial, JuradoExamen
from .forms import FormularioDirectorTesis, FormularioComiteTutorial, FormularioJuradoExamen
from apps.cuentas.decoradores import rol_requerido
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import ValidationError

ROLES_TODO = ['ADMIN', 'COORDINADOR', 'SECRETARIA']
ROLES_ESCRITURA = ['ADMIN', 'SECRETARIA']
ROLES_ADMIN = ['ADMIN']
ROLES_RESULTADO = ['ADMIN', 'COORDINADOR']

# --- DIRECTORES DE TESIS ---

@method_decorator(rol_requerido(*ROLES_TODO), name='dispatch')
class ListaDirectoresTesis(ListView):
    model = DirectorTesis
    template_name = 'tesis/lista_directores.html'
    context_object_name = 'directores'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('estudiante__persona', 'profesor__persona', 'estudiante__programa')
        programa_id = self.request.GET.get('programa')
        estado = self.request.GET.get('estado')
        
        if programa_id:
            qs = qs.filter(estudiante__programa_id=programa_id)
        if estado == 'activo':
            qs = qs.filter(activo=True)
        elif estado == 'inactivo':
            qs = qs.filter(activo=False)
            
        return qs.order_by('-fecha_asignacion')

@method_decorator(rol_requerido(*ROLES_ESCRITURA), name='dispatch')
class AsignarDirectorTesis(CreateView):
    model = DirectorTesis
    form_class = FormularioDirectorTesis
    template_name = 'tesis/form_director.html'
    success_url = reverse_lazy('tesis:lista_directores')

    def form_valid(self, form):
        try:
            # Model clean() is called automatically by form, but catch IntegrityError just in case
            return super().form_valid(form)
        except IntegrityError:
            form.add_error(None, 'Este profesor ya dirige a este estudiante.')
            return self.form_invalid(form)

@method_decorator(rol_requerido(*ROLES_ESCRITURA), name='dispatch')
class EditarDirectorTesis(UpdateView):
    model = DirectorTesis
    fields = ['fecha_termino', 'activo']
    template_name = 'tesis/form_director.html'
    success_url = reverse_lazy('tesis:lista_directores')

@method_decorator(rol_requerido(*ROLES_ADMIN), name='dispatch')
class DesactivarDirectorTesis(View):
    def post(self, request, pk):
        director = get_object_or_404(DirectorTesis, pk=pk)
        director.activo = False
        director.fecha_termino = timezone.now().date()
        director.save()
        messages.success(request, 'Director desactivado correctamente.')
        return redirect('tesis:lista_directores')

# --- COMITÉ TUTORIAL ---

@method_decorator(rol_requerido(*ROLES_TODO), name='dispatch')
class ListaComiteTutorial(ListView):
    model = ComiteTutorial
    template_name = 'tesis/lista_comite.html'
    context_object_name = 'comites'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('estudiante__persona', 'profesor__persona')
        estudiante_id = self.request.GET.get('estudiante')
        estado = self.request.GET.get('estado')
        
        if estudiante_id:
            qs = qs.filter(estudiante_id=estudiante_id)
        if estado == 'activo':
            qs = qs.filter(activo=True)
        elif estado == 'inactivo':
            qs = qs.filter(activo=False)
            
        return qs.order_by('-fecha_asignacion')

@method_decorator(rol_requerido(*ROLES_ESCRITURA), name='dispatch')
class AsignarComiteTutorial(CreateView):
    model = ComiteTutorial
    form_class = FormularioComiteTutorial
    template_name = 'tesis/form_comite.html'
    success_url = reverse_lazy('tesis:lista_comite')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            estudiante = form.cleaned_data['estudiante']
            miembros_activos = ComiteTutorial.objects.filter(estudiante=estudiante, activo=True).count()
            if miembros_activos >= 3:
                messages.warning(self.request, f'El comité de {estudiante.persona.nombre_completo} cuenta ahora con {miembros_activos} miembros activos.')
            return response
        except IntegrityError:
            form.add_error(None, 'Este profesor ya es miembro del comité tutorial de este estudiante.')
            return self.form_invalid(form)

@method_decorator(rol_requerido(*ROLES_ESCRITURA), name='dispatch')
class EditarComiteTutorial(UpdateView):
    model = ComiteTutorial
    fields = ['fecha_termino', 'activo']
    template_name = 'tesis/form_comite.html'
    success_url = reverse_lazy('tesis:lista_comite')

# --- JURADO DE EXAMEN ---

@method_decorator(rol_requerido(*ROLES_TODO), name='dispatch')
class ListaJuradoExamen(ListView):
    model = JuradoExamen
    template_name = 'tesis/lista_jurado.html'
    context_object_name = 'jurados'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('estudiante__persona', 'profesor__persona')
        tipo_examen = self.request.GET.get('tipo_examen')
        resultado = self.request.GET.get('resultado')
        
        if tipo_examen:
            qs = qs.filter(tipo_examen=tipo_examen)
        if resultado:
            qs = qs.filter(resultado=resultado)
            
        return qs.order_by('-fecha_examen', 'estudiante')

@method_decorator(rol_requerido(*ROLES_ESCRITURA), name='dispatch')
class AsignarJuradoExamen(CreateView):
    model = JuradoExamen
    form_class = FormularioJuradoExamen
    template_name = 'tesis/form_jurado.html'
    success_url = reverse_lazy('tesis:lista_jurado')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error(None, 'Este profesor ya forma parte de este jurado.')
            return self.form_invalid(form)

@method_decorator(rol_requerido(*ROLES_ESCRITURA), name='dispatch')
class EditarJuradoExamen(UpdateView):
    model = JuradoExamen
    fields = ['rol', 'fecha_examen', 'resultado']
    template_name = 'tesis/form_jurado.html'
    success_url = reverse_lazy('tesis:lista_jurado')

@method_decorator(rol_requerido(*ROLES_RESULTADO), name='dispatch')
class RegistrarResultadoExamen(View):
    def get(self, request, pk):
        # We pass a jurado item to identify the group. Wait, the route is /tesis/jurado/<int:pk>/resultado/
        # Since the jurado is per student and exam type, pk could be any of the jurado members.
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
                messages.success(request, 'Todos los miembros del jurado han aprobado. El estado del estudiante ha cambiado automáticamente a EGRESADO.')
        else:
            messages.info(request, 'Los resultados del jurado han sido guardados.')
            
        return redirect('tesis:lista_jurado')
