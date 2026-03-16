from django.test import TestCase, Client
from django.urls import reverse
from apps.cuentas.models import Usuario


class TestNombramientos(TestCase):
    def setUp(self):
        self.cliente = Client()
        self.usuario_coord = Usuario.objects.create_user(username='coord1', password='pass', rol=Usuario.Roles.COORDINADOR)
        self.usuario_secr = Usuario.objects.create_user(username='secr1', password='pass', rol=Usuario.Roles.SECRETARIA)

    def test_exportar_nombramientos_csv_coordinador_200(self):
        self.cliente.login(username='coord1', password='pass')
        respuesta = self.cliente.get(reverse('nombramientos:exportar_nombramientos_csv'))
        self.assertEqual(respuesta.status_code, 200)

    def test_exportar_nombramientos_csv_secretaria_403(self):
        self.cliente.login(username='secr1', password='pass')
        respuesta = self.cliente.get(reverse('nombramientos:exportar_nombramientos_csv'))
        self.assertEqual(respuesta.status_code, 403)
