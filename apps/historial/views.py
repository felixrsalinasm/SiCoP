from django.views.generic import ListView
from django.utils.decorators import method_decorator
from apps.cuentas.decoradores import rol_requerido
from .models import Registro

ROLES_ADMIN_COORD = ['ADMIN', 'COORDINADOR']

@method_decorator(rol_requerido(*ROLES_ADMIN_COORD), name='dispatch')
class VistaListaRegistros(ListView):
    model = Registro
    template_name = 'historial/lista.html'
    context_object_name = 'registros'
    paginate_by = 30
