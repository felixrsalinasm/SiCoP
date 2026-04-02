import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.cuentas.models import Usuario
from apps.personas.models import Persona, Profesor, Estudiante
from apps.programas.models import Programa, Laboratorio, Coordinador
from apps.nombramientos.models import Nombramiento, CatTipoNombramiento
from apps.tesis.models import Tesis, DirectorTesis, ComiteTutorial, JuradoExamen
from apps.historial.models import Registro


def obtener_permisos(modelos, acciones):
    permisos = []
    for modelo in modelos:
        ct = ContentType.objects.get_for_model(modelo)
        for accion in acciones:
            codename = f'{accion}_{ct.model}'
            perm = Permission.objects.filter(content_type=ct, codename=codename).first()
            if perm:
                permisos.append(perm)
    return permisos


def crear_grupos():
    print('  Creando grupos de permisos...')

    todos_los_modelos = [
        Persona, Profesor, Estudiante, Programa, Laboratorio, Coordinador,
        CatTipoNombramiento, Nombramiento, Tesis, DirectorTesis,
        ComiteTutorial, JuradoExamen, Registro
    ]

    grupo_admin, _ = Group.objects.get_or_create(name='Administrador')
    grupo_admin.permissions.set(
        obtener_permisos(todos_los_modelos, ['add', 'change', 'delete', 'view'])
    )

    modelos_secretaria = [Persona, Profesor, Estudiante, Tesis, Nombramiento]
    grupo_sec, _ = Group.objects.get_or_create(name='Secretaria')
    grupo_sec.permissions.set(
        obtener_permisos(modelos_secretaria, ['add', 'change', 'view'])
    )

    modelos_profesor = [Tesis, ComiteTutorial, Profesor]
    grupo_prof, _ = Group.objects.get_or_create(name='Profesor')
    grupo_prof.permissions.set(
        obtener_permisos(modelos_profesor, ['view'])
    )


def crear_datos_prueba():
    print('Iniciando carga de datos de prueba...')

    crear_grupos()

    grupo_admin = Group.objects.get(name='Administrador')
    grupo_sec = Group.objects.get(name='Secretaria')
    grupo_prof = Group.objects.get(name='Profesor')

    user_super, created = Usuario.objects.get_or_create(
        username='admin',
        defaults={'rol': Usuario.Roles.ADMIN, 'is_staff': True, 'is_superuser': True}
    )
    if created:
        user_super.set_password('Admin1234!')
        user_super.save()
        print('  Superusuario admin')

    user_adm, created = Usuario.objects.get_or_create(
        username='administrador1',
        defaults={'rol': Usuario.Roles.ADMIN}
    )
    if created:
        user_adm.set_password('Adm1n1234!')
        user_adm.save()
        print('  Usuario administrador1')
    user_adm.groups.add(grupo_admin)

    user_sec, created = Usuario.objects.get_or_create(
        username='secretaria1',
        defaults={'rol': Usuario.Roles.SECRETARIA}
    )
    if created:
        user_sec.set_password('Secr1234!')
        user_sec.save()
        print('  Usuario secretaria1')
    user_sec.groups.add(grupo_sec)

    user_p1, created = Usuario.objects.get_or_create(
        username='profesor1', defaults={'rol': Usuario.Roles.PROFESOR}
    )
    if created:
        user_p1.set_password('Prof1234!')
        user_p1.save()
    user_p1.groups.add(grupo_prof)

    user_p2, created = Usuario.objects.get_or_create(
        username='profesor2', defaults={'rol': Usuario.Roles.PROFESOR}
    )
    if created:
        user_p2.set_password('Prof1234!')
        user_p2.save()
    user_p2.groups.add(grupo_prof)

    print('  Laboratorios...')
    lab_lia, _ = Laboratorio.objects.get_or_create(
        siglas='LIA', defaults={'nombre': 'Laboratorio de Inteligencia Artificial'}
    )
    lab_lci, _ = Laboratorio.objects.get_or_create(
        siglas='LCI', defaults={'nombre': 'Laboratorio de Computo Inteligente'}
    )

    print('  Personas y profesores...')
    datos_profesores = [
        {
            'nombres': 'Juan Carlos', 'paterno': 'Reyes', 'materno': 'Morales',
            'email': 'jcreyes@cic.ipn.mx', 'genero': 'M', 'num_emp': '10234',
            'usuario': user_p1, 'lab': lab_lia
        },
        {
            'nombres': 'Maria Elena', 'paterno': 'Vazquez', 'materno': 'Torres',
            'email': 'mevazquez@cic.ipn.mx', 'genero': 'F', 'num_emp': '10235',
            'usuario': user_p2, 'lab': lab_lia
        },
        {
            'nombres': 'Roberto', 'paterno': 'Sanchez', 'materno': 'Avila',
            'email': 'rsanchez@cic.ipn.mx', 'genero': 'M', 'num_emp': '10236',
            'usuario': None, 'lab': lab_lci
        },
        {
            'nombres': 'Adriana', 'paterno': 'Lopez', 'materno': 'Fuentes',
            'email': 'alopez@cic.ipn.mx', 'genero': 'F', 'num_emp': '10237',
            'usuario': None, 'lab': lab_lci
        },
        {
            'nombres': 'Miguel Angel', 'paterno': 'Hernandez', 'materno': 'Cruz',
            'email': 'mahernandez@cic.ipn.mx', 'genero': 'M', 'num_emp': '10238',
            'usuario': None, 'lab': lab_lia
        },
        {
            'nombres': 'Laura Patricia', 'paterno': 'Gomez', 'materno': 'Rios',
            'email': 'lpgomez@cic.ipn.mx', 'genero': 'F', 'num_emp': '10239',
            'usuario': None, 'lab': lab_lci
        },
    ]

    profesores = []
    for dp in datos_profesores:
        persona, _ = Persona.objects.get_or_create(
            email=dp['email'],
            defaults={
                'nombres': dp['nombres'], 'paterno': dp['paterno'], 'materno': dp['materno'],
                'genero': dp['genero'], 'usuario': dp['usuario']
            }
        )
        prof, _ = Profesor.objects.get_or_create(
            persona=persona,
            defaults={
                'grado_academico': 'DOCTORADO', 'laboratorio': dp['lab'],
                'activo': True, 'numero_empleado': dp['num_emp'],
                'departamento': 'Ciencias de la Computacion'
            }
        )
        profesores.append(prof)

    reyes, vazquez, sanchez, lopez, hernandez, gomez = profesores

    persona_adm, _ = Persona.objects.get_or_create(
        email='administrador@cic.ipn.mx',
        defaults={
            'nombres': 'Administrador', 'paterno': 'Sistema', 'materno': 'CIC',
            'genero': 'NE', 'usuario': user_adm
        }
    )
    persona_sec, _ = Persona.objects.get_or_create(
        email='secretaria@cic.ipn.mx',
        defaults={
            'nombres': 'Ana', 'paterno': 'Torres', 'materno': 'Vega',
            'genero': 'F', 'usuario': user_sec
        }
    )

    print('  Programas...')
    prog_mcc, _ = Programa.objects.get_or_create(
        siglas='MCC',
        defaults={
            'nombre': 'Maestria en Ciencias en Computacion',
            'nivel': 'MAESTRIA', 'duracion_maxima_meses': 30, 'activo': True
        }
    )
    prog_dcc, _ = Programa.objects.get_or_create(
        siglas='DCC',
        defaults={
            'nombre': 'Doctorado en Ciencias en Computacion',
            'nivel': 'DOCTORADO', 'duracion_maxima_meses': 48, 'activo': True
        }
    )
    prog_ddcc, _ = Programa.objects.get_or_create(
        siglas='DDCC',
        defaults={
            'nombre': 'Doctorado Directo en Ciencias en Computacion',
            'nivel': 'DOCTORADO_DIRECTO', 'duracion_maxima_meses': 60, 'activo': True
        }
    )

    print('  Coordinadores...')
    Coordinador.objects.get_or_create(
        profesor=reyes, programa=prog_mcc,
        defaults={'fecha_inicio': '2023-01-01'}
    )

    print('  Tipos de nombramiento...')
    tipos_nombramiento = [
        ('Profesor de Posgrado', 'IPN'),
        ('Director de Tesis', 'IPN'),
        ('Codirector de Tesis', 'IPN'),
        ('Coordinador de Programa de Posgrado', 'IPN'),
        ('Miembro de Comite Tutorial', 'IPN'),
        ('Sinodal de Examen de Grado', 'IPN'),
        ('Profesor Visitante', 'EXTERNO'),
    ]
    for nombre, origen in tipos_nombramiento:
        CatTipoNombramiento.objects.get_or_create(
            nombramiento=nombre, defaults={'origen': origen}
        )

    tipo_pp = CatTipoNombramiento.objects.get(nombramiento='Profesor de Posgrado')

    print('  Nombramientos vigentes...')
    for prof in profesores:
        Nombramiento.objects.get_or_create(
            profesor=prof, tipo=tipo_pp,
            defaults={
                'clave': f'PPC-{prof.numero_empleado}',
                'fecha_inicio': '2024-01-01',
                'fecha_emision': '2024-01-01',
            }
        )

    print('  Alumnos...')
    datos_alumnos = [
        {
            'nombres': 'Carlos Alberto', 'paterno': 'Mendoza', 'materno': 'Perez',
            'email': 'camendoza@alumno.ipn.mx', 'genero': 'M',
            'matricula': 'A200100001', 'programa': prog_mcc,
            'generacion': 2023, 'fecha_ingreso': '2023-08-01'
        },
        {
            'nombres': 'Diana', 'paterno': 'Flores', 'materno': 'Castillo',
            'email': 'dflores@alumno.ipn.mx', 'genero': 'F',
            'matricula': 'A200100002', 'programa': prog_dcc,
            'generacion': 2022, 'fecha_ingreso': '2022-08-01'
        },
        {
            'nombres': 'Fernando', 'paterno': 'Rojas', 'materno': 'Jimenez',
            'email': 'frojas@alumno.ipn.mx', 'genero': 'M',
            'matricula': 'A200100003', 'programa': prog_ddcc,
            'generacion': 2021, 'fecha_ingreso': '2021-08-01'
        },
        {
            'nombres': 'Sofia', 'paterno': 'Guerrero', 'materno': 'Medina',
            'email': 'sguerrero@alumno.ipn.mx', 'genero': 'F',
            'matricula': 'A200100004', 'programa': prog_mcc,
            'generacion': 2024, 'fecha_ingreso': '2024-02-01'
        },
    ]

    estudiantes = []
    for da in datos_alumnos:
        persona, _ = Persona.objects.get_or_create(
            email=da['email'],
            defaults={
                'nombres': da['nombres'], 'paterno': da['paterno'], 'materno': da['materno'],
                'genero': da['genero']
            }
        )
        est, _ = Estudiante.objects.get_or_create(
            matricula=da['matricula'],
            defaults={
                'persona': persona, 'programa': da['programa'],
                'generacion': da['generacion'], 'modalidad': 'TC',
                'estado': 'ACTIVO', 'fecha_ingreso': da['fecha_ingreso']
            }
        )
        estudiantes.append(est)

    carlos, diana, fernando, sofia = estudiantes

    print('  Tesis...')
    tesis1, _ = Tesis.objects.get_or_create(
        titulo='Modelo de deteccion de anomalias en redes usando aprendizaje profundo',
        defaults={
            'estado': 'EN_PROCESO', 'fecha_registro': '2023-09-01',
            'alumno': carlos, 'programa': prog_mcc
        }
    )
    tesis2, _ = Tesis.objects.get_or_create(
        titulo='Optimizacion de algoritmos evolutivos para problemas de ruteo',
        defaults={
            'estado': 'EN_PROCESO', 'fecha_registro': '2022-09-01',
            'alumno': diana, 'programa': prog_dcc
        }
    )
    tesis3, _ = Tesis.objects.get_or_create(
        titulo='Sistemas de razonamiento automatico basados en logica difusa',
        defaults={
            'estado': 'CONCLUIDA', 'fecha_registro': '2021-09-01',
            'alumno': fernando, 'programa': prog_ddcc
        }
    )
    tesis4, _ = Tesis.objects.get_or_create(
        titulo='Clasificacion de patrones de comportamiento en redes sociales mediante redes neuronales',
        defaults={
            'estado': 'EN_PROCESO', 'fecha_registro': '2024-03-01',
            'alumno': sofia, 'programa': prog_mcc
        }
    )

    print('  Directores de tesis...')
    DirectorTesis.objects.get_or_create(
        tesis=tesis1, profesor=reyes,
        defaults={'tipo_direccion': 'DIRECTOR', 'fecha_asignacion': '2023-09-01'}
    )
    DirectorTesis.objects.get_or_create(
        tesis=tesis2, profesor=vazquez,
        defaults={'tipo_direccion': 'DIRECTOR', 'fecha_asignacion': '2022-09-01'}
    )
    DirectorTesis.objects.get_or_create(
        tesis=tesis2, profesor=sanchez,
        defaults={'tipo_direccion': 'CODIRECTOR', 'fecha_asignacion': '2022-09-15'}
    )
    DirectorTesis.objects.get_or_create(
        tesis=tesis3, profesor=sanchez,
        defaults={'tipo_direccion': 'DIRECTOR', 'fecha_asignacion': '2021-09-01'}
    )
    DirectorTesis.objects.get_or_create(
        tesis=tesis4, profesor=reyes,
        defaults={'tipo_direccion': 'DIRECTOR', 'fecha_asignacion': '2024-03-01'}
    )

    print('  Comites tutoriales...')
    ComiteTutorial.objects.get_or_create(
        tesis=tesis1, profesor=reyes,
        defaults={'rol': 'Director', 'fecha_asignacion': '2023-09-01'}
    )
    ComiteTutorial.objects.get_or_create(
        tesis=tesis1, profesor=vazquez,
        defaults={'rol': 'Vocal', 'fecha_asignacion': '2023-09-15'}
    )
    ComiteTutorial.objects.get_or_create(
        tesis=tesis1, profesor=sanchez,
        defaults={'rol': 'Vocal', 'fecha_asignacion': '2023-09-15'}
    )

    ComiteTutorial.objects.get_or_create(
        tesis=tesis2, profesor=vazquez,
        defaults={'rol': 'Directora', 'fecha_asignacion': '2022-09-01'}
    )
    ComiteTutorial.objects.get_or_create(
        tesis=tesis2, profesor=reyes,
        defaults={'rol': 'Vocal', 'fecha_asignacion': '2022-09-15'}
    )
    ComiteTutorial.objects.get_or_create(
        tesis=tesis2, profesor=lopez,
        defaults={'rol': 'Vocal', 'fecha_asignacion': '2022-09-15'}
    )
    ComiteTutorial.objects.get_or_create(
        tesis=tesis2, profesor=hernandez,
        defaults={'rol': 'Vocal', 'fecha_asignacion': '2022-09-15'}
    )

    print('  Jurado de examen...')
    jurado_data = [
        (fernando, lopez, 'PRESIDENTE'),
        (fernando, vazquez, 'SECRETARIO'),
        (fernando, reyes, 'VOCAL'),
        (fernando, hernandez, 'VOCAL'),
        (fernando, sanchez, 'VOCAL'),
        (fernando, gomez, 'SUPLENTE'),
    ]
    for alumno, prof, rol_jurado in jurado_data:
        JuradoExamen.objects.get_or_create(
            estudiante=alumno, profesor=prof, tipo_examen='GRADO',
            defaults={'rol': rol_jurado, 'fecha_examen': '2025-06-15', 'resultado': 'APROBADO'}
        )

    if Registro.objects.count() == 0:
        Registro.objects.create(
            usuario=user_adm, accion='CREAR', modulo='Tesis',
            descripcion='Registrar tesis: Modelo de deteccion de anomalias', ip='127.0.0.1'
        )

    print('Datos de prueba cargados correctamente.')


if __name__ == '__main__':
    crear_datos_prueba()
