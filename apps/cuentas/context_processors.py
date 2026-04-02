def grupos_usuario(request):
    if not hasattr(request, 'user') or not request.user.is_authenticated:
        return {
            'es_grupo_admin': False,
            'es_grupo_secretaria': False,
            'es_grupo_profesor': False,
        }
    user = request.user
    nombres = set(user.groups.values_list('name', flat=True))
    return {
        'es_grupo_admin': user.is_superuser or 'Administrador' in nombres,
        'es_grupo_secretaria': 'Secretaria' in nombres,
        'es_grupo_profesor': 'Profesor' in nombres,
    }
