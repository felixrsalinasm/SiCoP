from django.test import TestCase, Client
from django.urls import reverse
from apps.cuentas.models import Usuario


class TestCuentas(TestCase):
    def setUp(self):
        self.cliente = Client()
        self.usuario_profesor = Usuario.objects.create_user(
            username='testprof',
            password='Password123!',
            rol=Usuario.Roles.PROFESOR
        )
        self.usuario_admin = Usuario.objects.create_user(
            username='testadmin',
            password='Password123!',
            rol=Usuario.Roles.ADMIN
        )

    def test_acceso_no_autenticado_redirige_login(self):
        respuesta = self.cliente.get(reverse('cuentas:dashboard'))
        self.assertRedirects(respuesta, f"/cuentas/login/?next={reverse('cuentas:dashboard')}")

    def test_login_invalido_muestra_error(self):
        respuesta = self.cliente.post(reverse('cuentas:login'), {
            'username': 'testprof',
            'password': 'WrongPassword!'
        })
        self.assertEqual(respuesta.status_code, 200)
        self.assertTrue('form' in respuesta.context)
        self.assertTrue(respuesta.context['form'].errors)

    def test_login_correcto_admin_redirige_admin(self):
        respuesta = self.cliente.post(reverse('cuentas:login'), {
            'username': 'testadmin',
            'password': 'Password123!'
        })
        self.assertRedirects(respuesta, '/admin/', fetch_redirect_response=False)
