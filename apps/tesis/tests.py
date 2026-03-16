from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.cuentas.models import Usuario
from apps.personas.models import Persona, Profesor, Estudiante
from apps.programas.models import Programa
from apps.tesis.models import DirectorTesis, JuradoExamen


class TestTesis(TestCase):
    def setUp(self):
        self.cliente = Client()
        self.usuario_admin = Usuario.objects.create_superuser(username='admin1', password='p')

        self.prof1 = Profesor.objects.create(
            persona=Persona.objects.create(
                usuario=Usuario.objects.create_user(username='p1', password='p', rol=Usuario.Roles.PROFESOR),
                rfc='P1000AAAAAAA', curp='C10000000000000000', email='p1@ejemplo.com'
            ),
            activo=True
        )
        self.prof2 = Profesor.objects.create(
            persona=Persona.objects.create(
                usuario=Usuario.objects.create_user(username='p2', password='p', rol=Usuario.Roles.PROFESOR),
                rfc='P2000AAAAAAA', curp='C20000000000000000', email='p2@ejemplo.com'
            ),
            activo=True
        )
        self.prof3 = Profesor.objects.create(
            persona=Persona.objects.create(
                usuario=Usuario.objects.create_user(username='p3', password='p', rol=Usuario.Roles.PROFESOR),
                rfc='P3000AAAAAAA', curp='C30000000000000000', email='p3@ejemplo.com'
            ),
            activo=True
        )

        prog = Programa.objects.create(siglas='MCC', nombre='MCC', nivel='MAESTRIA', activo=True)
        self.est = Estudiante.objects.create(
            persona=Persona.objects.create(
                usuario=Usuario.objects.create_user(username='e1', password='p', rol=Usuario.Roles.SECRETARIA),
                rfc='E1000AAAAAAA', curp='C1000E000000000000', email='e1@ejemplo.com'
            ),
            programa=prog,
            matricula='A1',
            generacion=2024,
            fecha_ingreso=timezone.now().date()
        )

    def test_max_2_directores_activos(self):
        fecha = timezone.now().date()
        DirectorTesis.objects.create(estudiante=self.est, profesor=self.prof1, fecha_asignacion=fecha)
        DirectorTesis.objects.create(estudiante=self.est, profesor=self.prof2, fecha_asignacion=fecha)

        dir3 = DirectorTesis(estudiante=self.est, profesor=self.prof3, fecha_asignacion=fecha)
        with self.assertRaises(ValidationError):
            dir3.clean()

    def test_profesor_max_4_alumnos(self):
        fecha = timezone.now().date()
        prog = Programa.objects.create(siglas='DCC', nombre='DCC', nivel='DOCTORADO', activo=True)
        for i in range(4):
            e = Estudiante.objects.create(
                persona=Persona.objects.create(
                    usuario=Usuario.objects.create_user(username=f'e10{i}', password='p', rol=Usuario.Roles.SECRETARIA),
                    rfc=f'E100{i}AAAAAAA', curp=f'C100E{i}00000000000', email=f'e10{i}@ejemplo.com'
                ),
                programa=prog,
                matricula=f'A10{i}',
                generacion=2024,
                fecha_ingreso=timezone.now().date()
            )
            DirectorTesis.objects.create(estudiante=e, profesor=self.prof1, fecha_asignacion=fecha)

        dir_extra = DirectorTesis(estudiante=self.est, profesor=self.prof1, fecha_asignacion=fecha)
        with self.assertRaises(ValidationError):
            dir_extra.clean()

    def test_resultado_jurado_aprobado_egresa_estudiante(self):
        self.cliente.login(username='admin1', password='p')
        j1 = JuradoExamen.objects.create(estudiante=self.est, profesor=self.prof1, tipo_examen='GRADO', rol='PRESIDENTE')
        j2 = JuradoExamen.objects.create(estudiante=self.est, profesor=self.prof2, tipo_examen='GRADO', rol='SECRETARIO')

        respuesta = self.cliente.post(reverse('tesis:resultado_jurado', args=[j1.pk]), {
            f'resultado_{j1.pk}': 'APROBADO',
            f'resultado_{j2.pk}': 'APROBADO'
        })
        self.assertRedirects(respuesta, reverse('tesis:lista_jurado'))

        self.est.refresh_from_db()
        self.assertEqual(self.est.estado, 'EGRESADO')
