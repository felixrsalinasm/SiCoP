from .models import Registro

def registrar_accion(request, accion, modulo, descripcion):
    ip = request.META.get('REMOTE_ADDR')
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        
    Registro.objects.create(
        usuario=request.user if request.user.is_authenticated else None,
        accion=accion,
        modulo=modulo,
        descripcion=descripcion,
        ip=ip
    )
