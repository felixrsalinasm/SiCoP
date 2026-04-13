from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.urls import reverse

from apps.cuentas.models import Usuario


class TestNombramientos(TestCase):
    def setUp(self):
        self.cliente = Client()

        self.usuario_admin = Usuario.objects.create_user(username='admin1', password='pass', rol=Usuario.Roles.ADMIN)
        grupo_admin, _ = Group.objects.get_or_create(name='Administrador')
        self.usuario_admin.groups.add(grupo_admin)

        self.usuario_secr = Usuario.objects.create_user(username='secr1', password='pass', rol=Usuario.Roles.SECRETARIA)
        grupo_secr, _ = Group.objects.get_or_create(name='Secretaria')
        self.usuario_secr.groups.add(grupo_secr)

        self.usuario_prof = Usuario.objects.create_user(username='prof1', password='pass', rol=Usuario.Roles.PROFESOR)
        grupo_prof, _ = Group.objects.get_or_create(name='Profesor')
        self.usuario_prof.groups.add(grupo_prof)

    def test_exportar_nombramientos_csv_admin_200(self):
        self.cliente.login(username='admin1', password='pass')
        respuesta = self.cliente.get(reverse('nombramientos:exportar_nombramientos_csv'))
        self.assertEqual(respuesta.status_code, 200)

    def test_exportar_nombramientos_csv_secretaria_200(self):
        self.cliente.login(username='secr1', password='pass')
        respuesta = self.cliente.get(reverse('nombramientos:exportar_nombramientos_csv'))
        self.assertEqual(respuesta.status_code, 200)

    def test_exportar_nombramientos_csv_profesor_403(self):
        self.cliente.login(username='prof1', password='pass')
        respuesta = self.cliente.get(reverse('nombramientos:exportar_nombramientos_csv'))
        self.assertEqual(respuesta.status_code, 403)
