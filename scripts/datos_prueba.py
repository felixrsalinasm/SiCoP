import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.cuentas.models import Usuario
from apps.personas.models import Persona, Profesor, Estudiante
from apps.programas.models import Programa, Laboratorio
from apps.nombramientos.models import Nombramiento, CatTipoNombramiento, NombramientoProfesor
from apps.tesis.models import DirectorTesis, ComiteTutorial
from apps.historial.models import Registro


def crear_datos_prueba():
    print('Iniciando carga de datos de prueba...')

    user_coord, created = Usuario.objects.get_or_create(
        username='coordinador1',
        defaults={'rol': Usuario.Roles.COORDINADOR}
    )
    if created:
        user_coord.set_password('Coord1234!')
        user_coord.save()
        print('Creado usuario coordinador1')

    persona_coord, p_created = Persona.objects.get_or_create(
        email='cmendoza@cic.ipn.mx',
        defaults={
            'usuario': user_coord,
            'paterno': 'Mendoza',
            'materno': 'Reyes',
            'nombres': 'Carlos',
            'rfc': 'MERC800101XYZ',
            'curp': 'MERC800101HDFSXYZ1',
            'genero': 'M'
        }
    )
    if p_created:
        print('Creada persona Carlos Mendoza Reyes')

    user_sec, created = Usuario.objects.get_or_create(
        username='secretaria1',
        defaults={'rol': Usuario.Roles.SECRETARIA}
    )
    if created:
        user_sec.set_password('Secr1234!')
        user_sec.save()
        print('Creado usuario secretaria1')

    persona_sec, p_created = Persona.objects.get_or_create(
        email='atorres@cic.ipn.mx',
        defaults={
            'usuario': user_sec,
            'paterno': 'Torres',
            'materno': 'Vega',
            'nombres': 'Ana',
            'rfc': 'TOVA800201XYZ',
            'curp': 'TOVA800201MDFSXYZ1',
            'genero': 'F'
        }
    )
    if p_created:
        print('Creada persona Ana Torres Vega')

    user_p1, created = Usuario.objects.get_or_create(
        username='profesor1',
        defaults={'rol': Usuario.Roles.PROFESOR}
    )
    if created:
        user_p1.set_password('Prof1234!')
        user_p1.save()
        print('Creado usuario profesor1')

    persona_p1, p_created = Persona.objects.get_or_create(
        email='lramirez@cic.ipn.mx',
        defaults={
            'usuario': user_p1,
            'paterno': 'Ramirez',
            'materno': 'Castro',
            'nombres': 'Luis',
            'rfc': 'RACL700301XYZ',
            'curp': 'RACL700301HDFSXYZ1',
            'genero': 'M'
        }
    )
    if p_created:
        print('Creada persona Luis Ramirez Castro')

    lab_lia, _ = Laboratorio.objects.get_or_create(
        siglas='LIA',
        defaults={'nombre': 'Laboratorio de Inteligencia Artificial'}
    )
    profesor1, pr_created = Profesor.objects.get_or_create(
        persona=persona_p1,
        defaults={
            'grado_academico': 'DOCTORADO',
            'laboratorio': lab_lia,
            'activo': True
        }
    )
    if pr_created:
        print('Creado registro profesor: Luis Ramirez')

    user_p2, created = Usuario.objects.get_or_create(
        username='profesor2',
        defaults={'rol': Usuario.Roles.PROFESOR}
    )
    if created:
        user_p2.set_password('Prof1234!')
        user_p2.save()
        print('Creado usuario profesor2')

    persona_p2, p_created = Persona.objects.get_or_create(
        email='mgutierrez@cic.ipn.mx',
        defaults={
            'usuario': user_p2,
            'paterno': 'Gutierrez',
            'materno': 'Lopez',
            'nombres': 'Maria',
            'rfc': 'GULM700401XYZ',
            'curp': 'GULM700401MDFSXYZ1',
            'genero': 'F'
        }
    )
    if p_created:
        print('Creada persona Maria Gutierrez Lopez')

    lab_lci, _ = Laboratorio.objects.get_or_create(
        siglas='LCI',
        defaults={'nombre': 'Laboratorio de Computacion Inteligente'}
    )
    profesor2, pr_created = Profesor.objects.get_or_create(
        persona=persona_p2,
        defaults={
            'grado_academico': 'DOCTORADO',
            'laboratorio': lab_lci,
            'activo': True
        }
    )
    if pr_created:
        print('Creado registro profesor: Maria Gutierrez')

    prog_mcc, _ = Programa.objects.get_or_create(
        siglas='MCC',
        defaults={'nombre': 'Maestria en Ciencias de la Computacion', 'nivel': 'MAESTRIA'}
    )
    prog_dcc, _ = Programa.objects.get_or_create(
        siglas='DCC',
        defaults={'nombre': 'Doctorado en Ciencias de la Computacion', 'nivel': 'DOCTORADO'}
    )

    user_e1, _ = Usuario.objects.get_or_create(
        username='jcperez',
        defaults={'rol': Usuario.Roles.SECRETARIA}
    )
    persona_e1, _ = Persona.objects.get_or_create(
        email='jcperez@alumno.ipn.mx',
        defaults={
            'usuario': user_e1,
            'paterno': 'Perez',
            'materno': 'Morales',
            'nombres': 'Juan Carlos',
            'rfc': 'PEMJ900101XYZ',
            'curp': 'PEMJ900101HDFSXYZ1',
            'genero': 'M'
        }
    )
    estudiante1, e_created = Estudiante.objects.get_or_create(
        matricula='A230001',
        defaults={
            'persona': persona_e1,
            'programa': prog_mcc,
            'generacion': 2023,
            'modalidad': 'TC',
            'estado': 'ACTIVO',
            'fecha_ingreso': '2023-08-01'
        }
    )
    if e_created:
        print('Creado estudiante: Juan Carlos Perez')

    user_e2, _ = Usuario.objects.get_or_create(
        username='sevargas',
        defaults={'rol': Usuario.Roles.SECRETARIA}
    )
    persona_e2, _ = Persona.objects.get_or_create(
        email='sevargas@alumno.ipn.mx',
        defaults={
            'usuario': user_e2,
            'paterno': 'Vargas',
            'materno': 'Nunez',
            'nombres': 'Sofia Elena',
            'rfc': 'VANS900201XYZ',
            'curp': 'VANS900201MDFSXYZ1',
            'genero': 'F'
        }
    )
    estudiante2, e_created = Estudiante.objects.get_or_create(
        matricula='A230002',
        defaults={
            'persona': persona_e2,
            'programa': prog_dcc,
            'generacion': 2023,
            'modalidad': 'TC',
            'estado': 'ACTIVO',
            'fecha_ingreso': '2023-08-01'
        }
    )
    if e_created:
        print('Creado estudiante: Sofia Elena Vargas')

    tipo_nombramiento, _ = CatTipoNombramiento.objects.get_or_create(
        nombramiento='Investigador Nacional Nivel 1',
        origen='CONAHCYT'
    )

    nomb_p1, n_created = Nombramiento.objects.get_or_create(
        clave='SNI-2024-001',
        defaults={
            'tipo': tipo_nombramiento,
            'fecha_emision': '2024-01-01',
            'fecha_vencimiento': '2026-12-31'
        }
    )
    if n_created:
        print('Creado nombramiento SNI')

    NombramientoProfesor.objects.get_or_create(
        profesor=profesor1,
        nombramiento=nomb_p1
    )
    NombramientoProfesor.objects.get_or_create(
        profesor=profesor2,
        nombramiento=nomb_p1
    )

    DirectorTesis.objects.get_or_create(
        estudiante=estudiante1,
        profesor=profesor1,
        defaults={'fecha_asignacion': '2023-09-01'}
    )
    DirectorTesis.objects.get_or_create(
        estudiante=estudiante2,
        profesor=profesor2,
        defaults={'fecha_asignacion': '2023-09-01'}
    )
    ComiteTutorial.objects.get_or_create(
        estudiante=estudiante2,
        profesor=profesor1,
        defaults={'fecha_asignacion': '2023-09-15'}
    )
    ComiteTutorial.objects.get_or_create(
        estudiante=estudiante1,
        profesor=profesor2,
        defaults={'fecha_asignacion': '2023-09-15'}
    )

    if Registro.objects.count() == 0:
        Registro.objects.create(
            usuario=user_coord,
            accion='CREAR',
            modulo='Persona',
            descripcion='Crear registro: Perez Morales, Juan Carlos',
            ip='127.0.0.1'
        )
        Registro.objects.create(
            usuario=user_sec,
            accion='CREAR',
            modulo='Estudiante',
            descripcion='Crear registro: A230001 — Perez Morales, Juan Carlos',
            ip='127.0.0.1'
        )
        Registro.objects.create(
            usuario=user_coord,
            accion='EDITAR',
            modulo='Profesor',
            descripcion='Editar registro: Ramirez Castro, Luis',
            ip='127.0.0.1'
        )
        print('Creadas 3 entradas de historial')

    print('Datos de prueba cargados correctamente.')


if __name__ == '__main__':
    crear_datos_prueba()
