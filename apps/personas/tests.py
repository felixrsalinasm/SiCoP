from django.test import TestCase, Client
from django.urls import reverse
from apps.cuentas.models import Usuario
from apps.personas.models import Persona, Estudiante

class TestPersonas(TestCase):
    def setUp(self):
        self.cliente = Client()
        self.usuario_prof = Usuario.objects.create_user(username='prof1', password='pass', rol=Usuario.Roles.PROFESOR)
        self.usuario_secr = Usuario.objects.create_user(username='secr1', password='pass', rol=Usuario.Roles.SECRETARIA)
    
    def test_lista_personas_requiere_autenticacion(self):
        respuesta = self.cliente.get(reverse('personas:lista_personas'))
        self.assertRedirects(respuesta, "/dashboard/", fetch_redirect_response=False)

    def test_secretaria_puede_ver_lista(self):
        self.cliente.login(username='secr1', password='pass')
        respuesta = self.cliente.get(reverse('personas:lista_personas'))
        self.assertEqual(respuesta.status_code, 200)

    def test_profesor_no_puede_ver_lista(self):
        self.cliente.login(username='prof1', password='pass')
        respuesta = self.cliente.get(reverse('personas:lista_personas'))
        self.assertRedirects(respuesta, reverse('cuentas:dashboard'), fetch_redirect_response=False)

    def test_creacion_persona_invalida_rfc(self):
        self.cliente.login(username='secr1', password='pass')
        datos = {
            'usuario': self.usuario_prof.pk,
            'paterno': 'Perez',
            'materno': 'Gomez',
            'nombres': 'Juan',
            'rfc': 'P', # Inválido length
            'email': 'j@ipn.mx',
            'curp': 'PERJ800101XYZQWE12',
            'genero': 'M'
        }
        respuesta = self.cliente.post(reverse('personas:crear_persona'), datos)
        self.assertEqual(respuesta.status_code, 200) # Re-renders form
        self.assertTrue('form' in respuesta.context)
        self.assertIn('rfc', respuesta.context['form'].errors)
        
    def test_creacion_persona_valida(self):
        self.cliente.login(username='secr1', password='pass')
        datos = {
            'usuario': self.usuario_prof.pk,
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
