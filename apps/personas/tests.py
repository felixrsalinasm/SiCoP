from django.test import TestCase, Client
from django.urls import reverse
from apps.cuentas.models import Usuario
from apps.personas.models import Persona, Estudiante


class TestPersonas(TestCase):
    def setUp(self):
        self.cliente = Client()
        self.usuario_prof = Usuario.objects.create_user(username='prof1', password='pass', rol=Usuario.Roles.PROFESOR)
        self.usuario_secr = Usuario.objects.create_user(username='secr1', password='pass', rol=Usuario.Roles.SECRETARIA)
        self.usuario_coord = Usuario.objects.create_user(username='coord1', password='pass', rol=Usuario.Roles.COORDINADOR)

    def test_lista_personas_requiere_autenticacion(self):
        respuesta = self.cliente.get(reverse('personas:lista_personas'))
        self.assertEqual(respuesta.status_code, 302)

    def test_secretaria_puede_ver_lista(self):
        self.cliente.login(username='secr1', password='pass')
        respuesta = self.cliente.get(reverse('personas:lista_personas'))
        self.assertEqual(respuesta.status_code, 200)

    def test_profesor_no_puede_ver_lista(self):
        self.cliente.login(username='prof1', password='pass')
        respuesta = self.cliente.get(reverse('personas:lista_personas'))
        self.assertEqual(respuesta.status_code, 403)

    def test_creacion_persona_invalida_rfc(self):
        self.cliente.login(username='secr1', password='pass')
        datos = {
            'paterno': 'Perez',
            'materno': 'Gomez',
            'nombres': 'Juan',
            'rfc': 'P',
            'email': 'j@ipn.mx',
            'curp': 'PERJ800101XYZQWE12',
            'genero': 'M'
        }
        respuesta = self.cliente.post(reverse('personas:crear_persona'), datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertTrue('form' in respuesta.context)
        self.assertIn('rfc', respuesta.context['form'].errors)

    def test_creacion_persona_valida(self):
        self.cliente.login(username='secr1', password='pass')
        datos = {
            'paterno': 'Perez',
            'materno': 'Gomez',
            'nombres': 'Juan',
            'rfc': 'PERJ800101XYZ',
            'email': 'j@ipn.mx',
            'curp': 'PERJ800101XYZQWE12',
            'genero': 'M'
        }
        respuesta = self.cliente.post(reverse('personas:crear_persona'), datos)
        self.assertRedirects(respuesta, reverse('personas:lista_personas'))
        self.assertTrue(Persona.objects.filter(rfc='PERJ800101XYZ').exists())

    def test_exportar_profesores_csv_secretaria_200(self):
        self.cliente.login(username='secr1', password='pass')
        respuesta = self.cliente.get(reverse('personas:exportar_profesores_csv'))
        self.assertEqual(respuesta.status_code, 200)

    def test_exportar_profesores_csv_profesor_403(self):
        self.cliente.login(username='prof1', password='pass')
        respuesta = self.cliente.get(reverse('personas:exportar_profesores_csv'))
        self.assertEqual(respuesta.status_code, 403)

    def test_exportar_estudiantes_csv_coordinador_200(self):
        self.cliente.login(username='coord1', password='pass')
        respuesta = self.cliente.get(reverse('personas:exportar_estudiantes_csv'))
        self.assertEqual(respuesta.status_code, 200)

    def test_exportar_profesores_csv_content_disposition(self):
        self.cliente.login(username='secr1', password='pass')
        respuesta = self.cliente.get(reverse('personas:exportar_profesores_csv'))
        self.assertIn('attachment', respuesta['Content-Disposition'])
