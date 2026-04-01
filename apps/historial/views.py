from django.views.generic import ListView
from django.utils.decorators import method_decorator
from apps.cuentas.decoradores import grupo_requerido
from .models import Registro


@method_decorator(grupo_requerido('Administrador'), name='dispatch')
class VistaListaRegistros(ListView):
    model = Registro
    template_name = 'historial/lista.html'
    context_object_name = 'registros'
    paginate_by = 30
