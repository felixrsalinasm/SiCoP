from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q
from apps.personas.models import Profesor
from apps.programas.models import Programa
from apps.nombramientos.models import Nombramiento
from apps.tesis.models import DirectorTesis


class VistaLogin(LoginView):
    template_name = 'cuentas/login.html'

    def get_success_url(self):
        usuario = self.request.user
        if usuario.es_admin():
            return '/admin/'
        if usuario.es_profesor():
            if hasattr(usuario, 'persona') and hasattr(usuario.persona, 'profesor'):
                return f'/personas/profesores/{usuario.persona.profesor.pk}/'
            else:
                messages.warning(self.request, 'No tienes un perfil de profesor asociado en el sistema.')
                return '/dashboard/'
        return '/dashboard/'


class VistaLogout(LogoutView):
    next_page = '/cuentas/login/'


class VistaDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'cuentas/dashboard.html'
    login_url = '/cuentas/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user

        if hasattr(usuario, 'persona'):
            context['nombre_mostrar'] = usuario.persona.nombre_completo
        else:
            context['nombre_mostrar'] = usuario.username

        context['total_profesores_activos'] = Profesor.objects.filter(activo=True).count()

        context['programas_estudiantes'] = Programa.objects.annotate(
            estudiantes_activos=Count('estudiantes', filter=Q(estudiantes__estado='ACTIVO'))
        ).filter(activo=True)

        context['total_nombramientos_vigentes'] = Nombramiento.objects.filter(fecha_vencimiento__gte=timezone.now().date()).count()
        context['total_directores_activos'] = DirectorTesis.objects.filter(activo=True).count()

        return context
