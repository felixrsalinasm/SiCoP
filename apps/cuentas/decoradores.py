from django.shortcuts import redirect
from functools import wraps

def rol_requerido(*roles):
    def decorador(vista_func):
        @wraps(vista_func)
        def envoltorio(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.rol in roles:
                return vista_func(request, *args, **kwargs)
            return redirect('/dashboard/')
        return envoltorio
    return decorador
