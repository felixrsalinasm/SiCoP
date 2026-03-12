from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class VistaLogin(LoginView):
    template_name = 'cuentas/login.html'

    def get_success_url(self):
        usuario = self.request.user
        if usuario.es_admin():
            return '/admin/'
        return '/dashboard/'

class VistaLogout(LogoutView):
    next_page = '/cuentas/login/'

class VistaDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'cuentas/dashboard.html'
    login_url = '/cuentas/login/'
