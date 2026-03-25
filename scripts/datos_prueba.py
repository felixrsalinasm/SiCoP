import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.cuentas.models import Usuario
from apps.personas.models import Persona, Profesor, Estudiante
from apps.programas.models import Programa, Laboratorio
from apps.nombramientos.models import Nombramiento, CatTipoNombramiento
from apps.tesis.models import Tesis, DirectorTesis, ComiteTutorial
from apps.historial.models import Registro


def crear_datos_prueba():
    print('Iniciando carga de datos de prueba...')

    user_admin, created = Usuario.objects.get_or_create(
        username='admin',
        defaults={'rol': Usuario.Roles.ADMIN, 'is_staff': True, 'is_superuser': True}
    )
    if created:
        user_admin.set_password('Admin1234!')
        user_admin.save()
        print('  Usuario admin')
    else:
        if user_admin.rol != 'ADMIN':
            user_admin.rol = 'ADMIN'
            user_admin.save()



    user_coord, created = Usuario.objects.get_or_create(
        username='coordinador1',
        defaults={'rol': Usuario.Roles.COORDINADOR}
    )
    if created:
        user_coord.set_password('Coord1234!')
        user_coord.save()
        print('  Usuario coordinador1')

    persona_coord, _ = Persona.objects.get_or_create(
        email='cmendoza@cic.ipn.mx',
        defaults={
            'usuario': user_coord, 'paterno': 'Mendoza', 'materno': 'Reyes',
            'nombres': 'Carlos', 'rfc': 'MERC800101XYZ', 'curp': 'MERC800101HDFSXYZ1',
            'genero': 'M'
        }
    )

    user_sec, created = Usuario.objects.get_or_create(
        username='secretaria1',
        defaults={'rol': Usuario.Roles.SECRETARIA}
    )
    if created:
        user_sec.set_password('Secr1234!')
        user_sec.save()
        print('  Usuario secretaria1')

    Persona.objects.get_or_create(
        email='atorres@cic.ipn.mx',
        defaults={
            'usuario': user_sec, 'paterno': 'Torres', 'materno': 'Vega',
            'nombres': 'Ana', 'rfc': 'TOVA800201XYZ', 'curp': 'TOVA800201MDFSXYZ1',
            'genero': 'F'
        }
    )

    user_p1, created = Usuario.objects.get_or_create(
        username='profesor1', defaults={'rol': Usuario.Roles.PROFESOR}
    )
    if created:
        user_p1.set_password('Prof1234!')
        user_p1.save()

    persona_p1, _ = Persona.objects.get_or_create(
        email='lramirez@cic.ipn.mx',
        defaults={
            'usuario': user_p1, 'paterno': 'Ramirez', 'materno': 'Castro',
            'nombres': 'Luis', 'rfc': 'RACL700301XYZ', 'curp': 'RACL700301HDFSXYZ1',
            'genero': 'M'
        }
    )

    lab_lia, _ = Laboratorio.objects.get_or_create(siglas='LIA', defaults={'nombre': 'Laboratorio de Inteligencia Artificial'})
    profesor1, _ = Profesor.objects.get_or_create(
        persona=persona_p1,
        defaults={'grado_academico': 'DOCTORADO', 'laboratorio': lab_lia, 'activo': True,
                  'numero_empleado': 'EMP001', 'departamento': 'Ciencias de la Computacion'}
    )

    user_p2, created = Usuario.objects.get_or_create(
        username='profesor2', defaults={'rol': Usuario.Roles.PROFESOR}
    )
    if created:
        user_p2.set_password('Prof1234!')
        user_p2.save()

    persona_p2, _ = Persona.objects.get_or_create(
        email='mgutierrez@cic.ipn.mx',
        defaults={
            'usuario': user_p2, 'paterno': 'Gutierrez', 'materno': 'Lopez',
            'nombres': 'Maria', 'rfc': 'GULM700401XYZ', 'curp': 'GULM700401MDFSXYZ1',
            'genero': 'F'
        }
    )

    lab_lci, _ = Laboratorio.objects.get_or_create(siglas='LCI', defaults={'nombre': 'Laboratorio de Computacion Inteligente'})
    profesor2, _ = Profesor.objects.get_or_create(
        persona=persona_p2,
        defaults={'grado_academico': 'DOCTORADO', 'laboratorio': lab_lci, 'activo': True,
                  'numero_empleado': 'EMP002', 'departamento': 'Ciencias de la Computacion'}
    )

    user_p3, created = Usuario.objects.get_or_create(
        username='profesor3', defaults={'rol': Usuario.Roles.PROFESOR}
    )
    if created:
        user_p3.set_password('Prof1234!')
        user_p3.save()

    persona_p3, _ = Persona.objects.get_or_create(
        email='jherrera@cic.ipn.mx',
        defaults={
            'usuario': user_p3, 'paterno': 'Herrera', 'materno': 'Solis',
            'nombres': 'Jorge', 'rfc': 'HESJ750501XYZ', 'curp': 'HESJ750501HDFSXYZ1',
            'genero': 'M'
        }
    )

    profesor3, _ = Profesor.objects.get_or_create(
        persona=persona_p3,
        defaults={'grado_academico': 'DOCTORADO', 'laboratorio': lab_lia, 'activo': True,
                  'numero_empleado': 'EMP003', 'departamento': 'Sistemas Computacionales'}
    )

    prog_mcc, _ = Programa.objects.get_or_create(
        siglas='MCC',
        defaults={'nombre': 'Maestria en Ciencias de la Computacion', 'nivel': 'MAESTRIA', 'duracion_maxima_meses': 30}
    )
    prog_dcc, _ = Programa.objects.get_or_create(
        siglas='DCC',
        defaults={'nombre': 'Doctorado en Ciencias de la Computacion', 'nivel': 'DOCTORADO', 'duracion_maxima_meses': 48}
    )

    user_e1, _ = Usuario.objects.get_or_create(username='jcperez', defaults={'rol': Usuario.Roles.SECRETARIA})
    persona_e1, _ = Persona.objects.get_or_create(
        email='jcperez@alumno.ipn.mx',
        defaults={
            'usuario': user_e1, 'paterno': 'Perez', 'materno': 'Morales',
            'nombres': 'Juan Carlos', 'rfc': 'PEMJ900101XYZ', 'curp': 'PEMJ900101HDFSXYZ1',
            'genero': 'M'
        }
    )
    estudiante1, _ = Estudiante.objects.get_or_create(
        matricula='A230001',
        defaults={
            'persona': persona_e1, 'programa': prog_mcc, 'generacion': 2023,
            'modalidad': 'TC', 'estado': 'ACTIVO', 'fecha_ingreso': '2023-08-01'
        }
    )

    user_e2, _ = Usuario.objects.get_or_create(username='sevargas', defaults={'rol': Usuario.Roles.SECRETARIA})
    persona_e2, _ = Persona.objects.get_or_create(
        email='sevargas@alumno.ipn.mx',
        defaults={
            'usuario': user_e2, 'paterno': 'Vargas', 'materno': 'Nunez',
            'nombres': 'Sofia Elena', 'rfc': 'VANS900201XYZ', 'curp': 'VANS900201MDFSXYZ1',
            'genero': 'F'
        }
    )
    estudiante2, _ = Estudiante.objects.get_or_create(
        matricula='A230002',
        defaults={
            'persona': persona_e2, 'programa': prog_dcc, 'generacion': 2023,
            'modalidad': 'TC', 'estado': 'ACTIVO', 'fecha_ingreso': '2023-08-01'
        }
    )

    print('  Tipos de nombramiento IPN...')
    tipos_nombramiento = [
        ('Profesor de Posgrado Colegiado', 'IPN', 'Nombramiento para impartir cursos en programas de posgrado del IPN.'),
        ('Director de Tesis', 'IPN', 'Nombramiento formal para dirigir trabajos de tesis de posgrado.'),
        ('Coordinador de Programa', 'IPN', 'Responsable de la coordinacion academica de un programa de posgrado.'),
        ('Investigador Nacional', 'CONAHCYT', 'Distincion del Sistema Nacional de Investigadores del CONAHCyT.'),
        ('Investigador Nacional Emerito', 'CONAHCYT', 'Maximo nivel del Sistema Nacional de Investigadores.'),
        ('Profesor Invitado', 'EXTERNO', 'Profesor de otra institucion que participa en actividades de posgrado.'),
        ('Miembro de Comite Tutorial', 'IPN', 'Nombramiento para integrar comites tutoriales de posgrado.'),
    ]
    for nombre, origen, desc in tipos_nombramiento:
        CatTipoNombramiento.objects.get_or_create(
            nombramiento=nombre,
            defaults={'origen': origen, 'descripcion': desc}
        )

    tipo_director, _ = CatTipoNombramiento.objects.get_or_create(
        nombramiento='Director de Tesis', defaults={'origen': 'IPN'}
    )
    tipo_sni, _ = CatTipoNombramiento.objects.get_or_create(
        nombramiento='Investigador Nacional', defaults={'origen': 'CONAHCYT'}
    )

    nomb1, _ = Nombramiento.objects.get_or_create(
        clave='DIR-2024-001',
        defaults={
            'profesor': profesor1, 'tipo': tipo_director,
            'fecha_inicio': '2024-01-01', 'fecha_fin': '2026-12-31',
            'fecha_emision': '2024-01-01', 'fecha_vencimiento': '2026-12-31'
        }
    )
    nomb2, _ = Nombramiento.objects.get_or_create(
        clave='SNI-2024-001',
        defaults={
            'profesor': profesor1, 'tipo': tipo_sni,
            'fecha_inicio': '2024-01-01', 'fecha_fin': '2027-12-31',
            'fecha_emision': '2024-01-01', 'fecha_vencimiento': '2027-12-31'
        }
    )
    Nombramiento.objects.get_or_create(
        clave='DIR-2024-002',
        defaults={
            'profesor': profesor2, 'tipo': tipo_director,
            'fecha_inicio': '2024-01-01', 'fecha_fin': '2026-12-31',
            'fecha_emision': '2024-01-01', 'fecha_vencimiento': '2026-12-31'
        }
    )

    print('  Tesis...')
    tesis1, _ = Tesis.objects.get_or_create(
        titulo='Optimizacion de algoritmos de aprendizaje profundo para deteccion de objetos en tiempo real',
        defaults={
            'resumen': 'Investigacion sobre tecnicas de optimizacion aplicadas a redes neuronales convolucionales.',
            'estado': 'EN_PROCESO', 'fecha_registro': '2024-02-15',
            'alumno': estudiante1, 'programa': prog_mcc
        }
    )
    tesis2, _ = Tesis.objects.get_or_create(
        titulo='Modelos de lenguaje natural para el analisis semantico de textos cientificos en espanol',
        defaults={
            'resumen': 'Desarrollo de modelos NLP especializados en corpus cientifico hispanohablante.',
            'estado': 'EN_PROCESO', 'fecha_registro': '2024-03-01',
            'alumno': estudiante2, 'programa': prog_dcc
        }
    )

    print('  Directores y comites...')
    DirectorTesis.objects.get_or_create(
        tesis=tesis1, profesor=profesor1,
        defaults={'tipo_direccion': 'DIRECTOR', 'fecha_asignacion': '2024-02-15'}
    )
    DirectorTesis.objects.get_or_create(
        tesis=tesis2, profesor=profesor2,
        defaults={'tipo_direccion': 'DIRECTOR', 'fecha_asignacion': '2024-03-01'}
    )
    DirectorTesis.objects.get_or_create(
        tesis=tesis2, profesor=profesor1,
        defaults={'tipo_direccion': 'CODIRECTOR', 'fecha_asignacion': '2024-03-15'}
    )

    ComiteTutorial.objects.get_or_create(
        tesis=tesis1, profesor=profesor1,
        defaults={'rol': 'Director', 'fecha_asignacion': '2024-02-15'}
    )
    ComiteTutorial.objects.get_or_create(
        tesis=tesis1, profesor=profesor2,
        defaults={'rol': 'Investigador', 'fecha_asignacion': '2024-02-20'}
    )
    ComiteTutorial.objects.get_or_create(
        tesis=tesis1, profesor=profesor3,
        defaults={'rol': 'Investigador', 'fecha_asignacion': '2024-02-20'}
    )

    if Registro.objects.count() == 0:
        Registro.objects.create(
            usuario=user_sec, accion='CREAR', modulo='Tesis',
            descripcion='Crear registro: Optimizacion de algoritmos de aprendizaje profundo...', ip='127.0.0.1'
        )
        Registro.objects.create(
            usuario=user_coord, accion='CREAR', modulo='DirectorTesis',
            descripcion='Asignar: Ramirez Castro, Luis como director', ip='127.0.0.1'
        )
        Registro.objects.create(
            usuario=user_sec, accion='CREAR', modulo='Nombramiento',
            descripcion='Crear nombramiento: DIR-2024-001', ip='127.0.0.1'
        )
        print('  Historial de ejemplo')

    print('Datos de prueba cargados correctamente.')


if __name__ == '__main__':
    crear_datos_prueba()
