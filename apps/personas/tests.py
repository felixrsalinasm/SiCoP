from datetime import date

from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from apps.cuentas.models import Usuario
from apps.personas.models import Persona, Profesor, Estudiante
from apps.programas.models import Laboratorio, Programa


class TestPersonas(TestCase):
    def setUp(self):
        self.cliente = Client()

        self.usuario_prof = Usuario.objects.create_user(username='prof1', password='pass', rol=Usuario.Roles.PROFESOR)
        grupo_prof, _ = Group.objects.get_or_create(name='Profesor')
        self.usuario_prof.groups.add(grupo_prof)

        self.usuario_secr = Usuario.objects.create_user(username='secr1', password='pass', rol=Usuario.Roles.SECRETARIA)
        grupo_secr, _ = Group.objects.get_or_create(name='Secretaria')
        self.usuario_secr.groups.add(grupo_secr)

        self.usuario_admin = Usuario.objects.create_user(username='admin1', password='pass', rol=Usuario.Roles.ADMIN)
        grupo_admin, _ = Group.objects.get_or_create(name='Administrador')
        self.usuario_admin.groups.add(grupo_admin)

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

    def test_exportar_profesores_csv_secretaria_200(self):
        self.cliente.login(username='secr1', password='pass')
        respuesta = self.cliente.get(reverse('personas:exportar_profesores_csv'))
        self.assertEqual(respuesta.status_code, 200)

    def test_exportar_profesores_csv_profesor_403(self):
        self.cliente.login(username='prof1', password='pass')
        respuesta = self.cliente.get(reverse('personas:exportar_profesores_csv'))
        self.assertEqual(respuesta.status_code, 403)

    def test_exportar_estudiantes_csv_admin_200(self):
        self.cliente.login(username='admin1', password='pass')
        respuesta = self.cliente.get(reverse('personas:exportar_estudiantes_csv'))
        self.assertEqual(respuesta.status_code, 200)

    def test_exportar_profesores_csv_content_disposition(self):
        self.cliente.login(username='secr1', password='pass')
        respuesta = self.cliente.get(reverse('personas:exportar_profesores_csv'))
        self.assertIn('attachment', respuesta['Content-Disposition'])


class TestPersonaValidaciones(TestCase):
    def test_fecha_nacimiento_futura_rechazada(self):
        from datetime import timedelta
        persona = Persona(
            paterno='Garcia', materno='Lopez', nombres='Pedro',
            email='test_fut@ipn.mx',
            fecha_nacimiento=date.today() + timedelta(days=30)
        )
        with self.assertRaises(ValidationError) as ctx:
            persona.clean()
        self.assertIn('fecha_nacimiento', ctx.exception.message_dict)

    def test_curp_fecha_incorrecta_rechazada(self):
        persona = Persona(
            paterno='Reyes', materno='Morales', nombres='Juan',
            email='curp_fecha@ipn.mx',
            curp='REMJ800101HDFYRL09',
            fecha_nacimiento=date(1985, 6, 15)
        )
        with self.assertRaises(ValidationError) as ctx:
            persona.clean()
        self.assertIn('curp', ctx.exception.message_dict)

    def test_curp_fecha_correcta_aceptada(self):
        persona = Persona(
            paterno='Reyes', materno='Morales', nombres='Juan',
            email='curp_ok@ipn.mx',
            curp='REMJ800101HDFYRL09',
            fecha_nacimiento=date(1980, 1, 1)
        )
        try:
            persona.clean()
        except ValidationError as e:
            self.assertNotIn('curp', e.message_dict)

    def test_curp_genero_incorrecto_rechazado(self):
        persona = Persona(
            paterno='Reyes', materno='Morales', nombres='Juan',
            email='curp_gen@ipn.mx',
            curp='REMJ800101MDFYRL09',
            genero='M',
            fecha_nacimiento=date(1980, 1, 1)
        )
        with self.assertRaises(ValidationError) as ctx:
            persona.clean()
        self.assertIn('genero', ctx.exception.message_dict)

    def test_curp_inicial_paterno_incorrecta_rechazada(self):
        persona = Persona(
            paterno='Gonzalez', materno='Morales', nombres='Juan',
            email='curp_pat@ipn.mx',
            curp='REMJ800101HDFYRL09',
            fecha_nacimiento=date(1980, 1, 1)
        )
        with self.assertRaises(ValidationError) as ctx:
            persona.clean()
        self.assertIn('paterno', ctx.exception.message_dict)

    def test_rfc_fecha_distinta_rechazado(self):
        persona = Persona(
            paterno='Reyes', materno='Morales', nombres='Juan',
            email='rfc_fecha@ipn.mx',
            rfc='REMJ900101XYZ',
            fecha_nacimiento=date(1980, 1, 1)
        )
        with self.assertRaises(ValidationError) as ctx:
            persona.clean()
        self.assertIn('rfc', ctx.exception.message_dict)

    def test_consistencia_curp_rfc_rechazada(self):
        persona = Persona(
            paterno='Reyes', materno='Morales', nombres='Juan',
            email='curp_rfc@ipn.mx',
            curp='REMJ800101HDFYRL09',
            rfc='REMJ900101XYZ',
            fecha_nacimiento=date(1980, 1, 1)
        )
        with self.assertRaises(ValidationError) as ctx:
            persona.clean()
        self.assertIn('rfc', ctx.exception.message_dict)


class TestProfesorValidaciones(TestCase):
    def test_externo_con_laboratorio_rechazado(self):
        lab = Laboratorio.objects.create(nombre='Lab Test', siglas='LT')
        persona = Persona.objects.create(
            paterno='Test', materno='Lab', nombres='Uno', email='ext_lab@ipn.mx'
        )
        profesor = Profesor(
            persona=persona, grado_academico='DOCTORADO',
            es_externo=True, laboratorio=lab
        )
        with self.assertRaises(ValidationError) as ctx:
            profesor.clean()
        self.assertIn('laboratorio', ctx.exception.message_dict)

    def test_fecha_ingreso_cic_anterior_a_ipn_rechazada(self):
        persona = Persona.objects.create(
            paterno='Test', materno='Fecha', nombres='Dos', email='fecha_cic@ipn.mx'
        )
        profesor = Profesor(
            persona=persona, grado_academico='DOCTORADO',
            fecha_ingreso_ipn=date(2010, 1, 1),
            fecha_ingreso_cic=date(2005, 1, 1)
        )
        with self.assertRaises(ValidationError) as ctx:
            profesor.clean()
        self.assertIn('fecha_ingreso_cic', ctx.exception.message_dict)


class TestEstudianteValidaciones(TestCase):
    def setUp(self):
        self.prog_doc = Programa.objects.create(
            siglas='DCC_T', nombre='Doctorado Test', nivel='DOCTORADO', activo=True
        )
        self.prog_mae = Programa.objects.create(
            siglas='MCC_T', nombre='Maestria Test', nivel='MAESTRIA', activo=True
        )

    def test_doctorado_modalidad_tp_rechazado(self):
        persona = Persona.objects.create(
            paterno='Est', materno='Doc', nombres='TP', email='est_tp@ipn.mx'
        )
        estudiante = Estudiante(
            persona=persona, programa=self.prog_doc, matricula='T001',
            generacion=2024, modalidad='TP', estado='ACTIVO',
            fecha_ingreso=date(2024, 8, 1)
        )
        with self.assertRaises(ValidationError) as ctx:
            estudiante.clean()
        self.assertIn('modalidad', ctx.exception.message_dict)

    def test_egresado_sin_fecha_egreso_rechazado(self):
        persona = Persona.objects.create(
            paterno='Est', materno='Egr', nombres='SF', email='est_egr@ipn.mx'
        )
        estudiante = Estudiante(
            persona=persona, programa=self.prog_mae, matricula='T002',
            generacion=2024, modalidad='TC', estado='EGRESADO',
            fecha_ingreso=date(2024, 8, 1)
        )
        with self.assertRaises(ValidationError) as ctx:
            estudiante.clean()
        self.assertIn('fecha_egreso', ctx.exception.message_dict)

    def test_activo_con_fecha_egreso_rechazado(self):
        persona = Persona.objects.create(
            paterno='Est', materno='Act', nombres='FE', email='est_act@ipn.mx'
        )
        estudiante = Estudiante(
            persona=persona, programa=self.prog_mae, matricula='T003',
            generacion=2024, modalidad='TC', estado='ACTIVO',
            fecha_ingreso=date(2024, 8, 1), fecha_egreso=date(2025, 1, 1)
        )
        with self.assertRaises(ValidationError) as ctx:
            estudiante.clean()
        self.assertIn('fecha_egreso', ctx.exception.message_dict)

    def test_generacion_diferente_anio_ingreso_rechazada(self):
        persona = Persona.objects.create(
            paterno='Est', materno='Gen', nombres='Dif', email='est_gen@ipn.mx'
        )
        estudiante = Estudiante(
            persona=persona, programa=self.prog_mae, matricula='T004',
            generacion=2023, modalidad='TC', estado='ACTIVO',
            fecha_ingreso=date(2024, 8, 1)
        )
        with self.assertRaises(ValidationError) as ctx:
            estudiante.clean()
        self.assertIn('generacion', ctx.exception.message_dict)
