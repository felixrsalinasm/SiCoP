from django.test import TestCase, Client
from django.urls import reverse
from apps.cuentas.models import Usuario
from apps.personas.models import Persona
from apps.historial.models import Registro


class TestHistorial(TestCase):
    def setUp(self):
        self.cliente = Client()
        self.usuario_admin = Usuario.objects.create_user(username='admin1', password='pass', rol=Usuario.Roles.ADMIN)
        self.usuario_prof = Usuario.objects.create_user(username='prof1', password='pass', rol=Usuario.Roles.PROFESOR)
        self.usuario_secr = Usuario.objects.create_user(username='secr1', password='pass', rol=Usuario.Roles.SECRETARIA)

    def test_crear_persona_registra_historial(self):
        self.cliente.login(username='secr1', password='pass')
        datos = {
            'paterno': 'Lopez',
            'materno': 'Diaz',
            'nombres': 'Ana',
            'rfc': 'LODA900101XYZ',
            'email': 'ana@ipn.mx',
            'curp': 'LODA900101XYZQWE12',
            'genero': 'F'
        }
        self.cliente.post(reverse('personas:crear_persona'), datos)
        self.assertTrue(Registro.objects.filter(accion='CREAR', modulo='Persona').exists())

    def test_editar_persona_registra_historial(self):
        self.cliente.login(username='secr1', password='pass')
        persona = Persona.objects.create(
            paterno='Test', nombres='Edicion', email='edit@ipn.mx'
        )
        datos = {
            'paterno': 'Test',
            'materno': '',
            'nombres': 'Editado',
            'email': 'edit@ipn.mx',
            'genero': '',
        }
        self.cliente.post(reverse('personas:editar_persona', args=[persona.pk]), datos)
        self.assertTrue(Registro.objects.filter(accion='EDITAR', modulo='Persona').exists())

    def test_historial_vista_admin_200(self):
        self.cliente.login(username='admin1', password='pass')
        respuesta = self.cliente.get(reverse('historial:historial_lista'))
        self.assertEqual(respuesta.status_code, 200)

    def test_historial_vista_profesor_403(self):
        self.cliente.login(username='prof1', password='pass')
        respuesta = self.cliente.get(reverse('historial:historial_lista'))
        self.assertEqual(respuesta.status_code, 403)
