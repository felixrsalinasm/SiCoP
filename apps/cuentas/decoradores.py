from django.http import HttpResponseForbidden
from django.template.loader import render_to_string
from functools import wraps


def rol_requerido(*roles):
    def decorador(vista_func):
        @wraps(vista_func)
        def envoltorio(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.shortcuts import redirect
                return redirect('/cuentas/login/')
            if request.user.rol in roles:
                return vista_func(request, *args, **kwargs)
            return HttpResponseForbidden(render_to_string('403.html', request=request))
        return envoltorio
    return decorador


def grupo_requerido(*nombres_grupo):
    def decorador(vista_func):
        @wraps(vista_func)
        def envoltorio(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.shortcuts import redirect
                return redirect('/cuentas/login/')
            if request.user.is_superuser:
                return vista_func(request, *args, **kwargs)
            if request.user.groups.filter(name__in=nombres_grupo).exists():
                return vista_func(request, *args, **kwargs)
            return HttpResponseForbidden(render_to_string('403.html', request=request))
        return envoltorio
    return decorador
