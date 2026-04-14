from datetime import date

from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from apps.cuentas.models import Usuario
from apps.personas.models import Persona, Profesor, Estudiante
from apps.programas.models import Programa
from apps.nombramientos.models import Nombramiento, CatTipoNombramiento
from apps.tesis.models import Tesis, DirectorTesis, ComiteTutorial, JuradoExamen


class TestDirectorTesisValidaciones(TestCase):
    def setUp(self):
        self.prog_mae = Programa.objects.create(
            siglas='MCC_T', nombre='Maestria Test', nivel='MAESTRIA', activo=True
        )
        self.prog_doc = Programa.objects.create(
            siglas='DCC_T', nombre='Doctorado Test', nivel='DOCTORADO', activo=True
        )
        self.tipo_pp = CatTipoNombramiento.objects.create(
            nombramiento='Profesor de Posgrado', origen='IPN'
        )

        self.persona_est = Persona.objects.create(
            paterno='Alumno', materno='Test', nombres='Uno', email='a1_test@ipn.mx'
        )
        self.est = Estudiante.objects.create(
            persona=self.persona_est, programa=self.prog_mae,
            matricula='T100', generacion=2024, fecha_ingreso=date(2024, 8, 1)
        )
        self.tesis = Tesis.objects.create(
            titulo='Tesis de prueba', estado='EN_PROCESO',
            fecha_registro=date(2024, 9, 1), alumno=self.est, programa=self.prog_mae
        )

        self.prof1 = self._crear_profesor('Ext1', 'Test', 'ext1@ipn.mx', es_externo=True)
        self.prof2 = self._crear_profesor('Ext2', 'Test', 'ext2@ipn.mx', es_externo=True)
        self.prof_interno = self._crear_profesor('Int1', 'Test', 'int1@ipn.mx', es_externo=False)

        Nombramiento.objects.create(
            profesor=self.prof_interno, tipo=self.tipo_pp,
            clave='PPC-INT1', fecha_emision=date(2024, 1, 1)
        )

    def _crear_profesor(self, paterno, materno, email, es_externo=False):
        persona = Persona.objects.create(
            paterno=paterno, materno=materno, nombres='Prof', email=email
        )
        return Profesor.objects.create(
            persona=persona, grado_academico='DOCTORADO',
            es_externo=es_externo, activo=True
        )

    def test_dos_directores_externos_rechazados(self):
        DirectorTesis.objects.create(
            tesis=self.tesis, profesor=self.prof1,
            fecha_asignacion=date(2024, 9, 1), activo=True
        )
        dir2 = DirectorTesis(
            tesis=self.tesis, profesor=self.prof2,
            fecha_asignacion=date(2024, 9, 1), activo=True
        )
        with self.assertRaises(ValidationError) as ctx:
            dir2.clean()
        errores = ctx.exception.message_dict
        self.assertTrue(
            any('externo' in str(v).lower() for v in errores.values())
        )

    def test_max_2_directores_activos(self):
        prof3 = self._crear_profesor('P3', 'T', 'p3@ipn.mx')
        Nombramiento.objects.create(
            profesor=prof3, tipo=self.tipo_pp,
            clave='PPC-P3', fecha_emision=date(2024, 1, 1)
        )
        prof4 = self._crear_profesor('P4', 'T', 'p4@ipn.mx')
        Nombramiento.objects.create(
            profesor=prof4, tipo=self.tipo_pp,
            clave='PPC-P4', fecha_emision=date(2024, 1, 1)
        )
        prof5 = self._crear_profesor('P5', 'T', 'p5@ipn.mx')
        Nombramiento.objects.create(
            profesor=prof5, tipo=self.tipo_pp,
            clave='PPC-P5', fecha_emision=date(2024, 1, 1)
        )

        DirectorTesis.objects.create(
            tesis=self.tesis, profesor=prof3,
            fecha_asignacion=date(2024, 9, 1), activo=True
        )
        DirectorTesis.objects.create(
            tesis=self.tesis, profesor=prof4,
            fecha_asignacion=date(2024, 9, 1), activo=True
        )
        dir3 = DirectorTesis(
            tesis=self.tesis, profesor=prof5,
            fecha_asignacion=date(2024, 9, 1), activo=True
        )
        with self.assertRaises(ValidationError):
            dir3.clean()

    def test_director_inactivo_sin_fecha_termino_rechazado(self):
        prof_int = self._crear_profesor('Inact', 'T', 'inact@ipn.mx')
        Nombramiento.objects.create(
            profesor=prof_int, tipo=self.tipo_pp,
            clave='PPC-INACT', fecha_emision=date(2024, 1, 1)
        )
        director = DirectorTesis(
            tesis=self.tesis, profesor=prof_int,
            fecha_asignacion=date(2024, 9, 1), activo=False
        )
        with self.assertRaises(ValidationError) as ctx:
            director.clean()
        self.assertIn('fecha_termino', ctx.exception.message_dict)


class TestComiteTutorialValidaciones(TestCase):
    def test_especialidad_rechazada(self):
        prog_esp = Programa.objects.create(
            siglas='ESP_T', nombre='Especialidad Test', nivel='ESPECIALIDAD', activo=True
        )
        persona_est = Persona.objects.create(
            paterno='Est', materno='Esp', nombres='Uno', email='esp_est@ipn.mx'
        )
        est = Estudiante.objects.create(
            persona=persona_est, programa=prog_esp,
            matricula='T200', generacion=2024, fecha_ingreso=date(2024, 8, 1)
        )
        tesis = Tesis.objects.create(
            titulo='Tesis Especialidad', estado='EN_PROCESO',
            fecha_registro=date(2024, 9, 1), alumno=est, programa=prog_esp
        )
        persona_prof = Persona.objects.create(
            paterno='Prof', materno='Com', nombres='Uno', email='com_prof@ipn.mx'
        )
        prof = Profesor.objects.create(
            persona=persona_prof, grado_academico='DOCTORADO', activo=True
        )
        comite = ComiteTutorial(
            tesis=tesis, profesor=prof,
            fecha_asignacion=date(2024, 9, 1), activo=True
        )
        with self.assertRaises(ValidationError) as ctx:
            comite.clean()
        errores = ctx.exception.message_dict
        self.assertTrue(
            any('art. 22' in str(v).lower() for v in errores.values())
        )


class TestJuradoExamenValidaciones(TestCase):
    def setUp(self):
        self.prog_mae = Programa.objects.create(
            siglas='MCC_J', nombre='Maestria Jurado', nivel='MAESTRIA', activo=True
        )
        self.prog_doc = Programa.objects.create(
            siglas='DCC_J', nombre='Doctorado Jurado', nivel='DOCTORADO', activo=True
        )

    def _crear_estudiante(self, programa, matricula, email):
        persona = Persona.objects.create(
            paterno='Est', materno='Jur', nombres=matricula, email=email
        )
        return Estudiante.objects.create(
            persona=persona, programa=programa,
            matricula=matricula, generacion=2024, fecha_ingreso=date(2024, 8, 1)
        )

    def _crear_profesor_doctor(self, email):
        persona = Persona.objects.create(
            paterno='Prof', materno='Jur', nombres=email.split('@')[0], email=email
        )
        return Profesor.objects.create(
            persona=persona, grado_academico='DOCTORADO', activo=True
        )

    def test_predoctoral_para_maestria_rechazado(self):
        est = self._crear_estudiante(self.prog_mae, 'T300', 'pred_mae@ipn.mx')
        prof = self._crear_profesor_doctor('prof_pred@ipn.mx')
        jurado = JuradoExamen(
            estudiante=est, profesor=prof,
            tipo_examen='PREDOCTORAL', rol='PRESIDENTE'
        )
        with self.assertRaises(ValidationError) as ctx:
            jurado.clean()
        errores = ctx.exception.message_dict
        self.assertTrue(
            any('art. 25' in str(v).lower() for v in errores.values())
        )

    def test_resultado_aprobado_sin_fecha_rechazado(self):
        est = self._crear_estudiante(self.prog_mae, 'T301', 'res_sf@ipn.mx')
        prof = self._crear_profesor_doctor('prof_res@ipn.mx')
        jurado = JuradoExamen(
            estudiante=est, profesor=prof,
            tipo_examen='GRADO', rol='PRESIDENTE',
            resultado='APROBADO'
        )
        with self.assertRaises(ValidationError) as ctx:
            jurado.clean()
        self.assertIn('fecha_examen', ctx.exception.message_dict)


class TestMisEstudiantes(TestCase):
    def setUp(self):
        self.cliente = Client()

        self.programa = Programa.objects.create(
            siglas='MCC_ME', nombre='Maestria ME', nivel='MAESTRIA', activo=True
        )

        persona_prof1 = Persona.objects.create(
            paterno='Director', materno='Uno', nombres='Prof', email='dir1@ipn.mx'
        )
        self.prof1 = Profesor.objects.create(
            persona=persona_prof1, grado_academico='DOCTORADO', activo=True
        )
        self.usuario_prof1 = Usuario.objects.create_user(username='dirprof1', password='pass', rol=Usuario.Roles.PROFESOR)
        grupo_prof, _ = Group.objects.get_or_create(name='Profesor')
        self.usuario_prof1.groups.add(grupo_prof)
        persona_prof1.usuario = self.usuario_prof1
        persona_prof1.save()

        persona_prof2 = Persona.objects.create(
            paterno='Director', materno='Dos', nombres='Prof', email='dir2@ipn.mx'
        )
        self.prof2 = Profesor.objects.create(
            persona=persona_prof2, grado_academico='DOCTORADO', activo=True
        )

        persona_est = Persona.objects.create(
            paterno='Alumno', materno='ME', nombres='Uno', email='alumno_me@ipn.mx'
        )
        self.est = Estudiante.objects.create(
            persona=persona_est, programa=self.programa,
            matricula='ME001', generacion=2024, fecha_ingreso=date(2024, 8, 1)
        )
        self.tesis = Tesis.objects.create(
            titulo='Tesis ME Test', estado='EN_PROCESO',
            fecha_registro=date(2024, 9, 1), alumno=self.est, programa=self.programa
        )
        DirectorTesis.objects.create(
            tesis=self.tesis, profesor=self.prof1,
            fecha_asignacion=date(2024, 9, 1), activo=True
        )

        self.usuario_secr = Usuario.objects.create_user(username='secr1', password='pass', rol=Usuario.Roles.SECRETARIA)
        grupo_secr, _ = Group.objects.get_or_create(name='Secretaria')
        self.usuario_secr.groups.add(grupo_secr)

    def test_profesor_ve_mis_estudiantes_200(self):
        self.cliente.login(username='dirprof1', password='pass')
        respuesta = self.cliente.get(reverse('tesis:mis_estudiantes'))
        self.assertEqual(respuesta.status_code, 200)

    def test_profesor_solo_ve_sus_estudiantes(self):
        self.cliente.login(username='dirprof1', password='pass')
        respuesta = self.cliente.get(reverse('tesis:mis_estudiantes'))
        directores = respuesta.context['directores']
        for d in directores:
            self.assertEqual(d.profesor.pk, self.prof1.pk)

    def test_secretaria_ve_mis_estudiantes_200(self):
        self.cliente.login(username='secr1', password='pass')
        respuesta = self.cliente.get(reverse('tesis:mis_estudiantes'))
        self.assertEqual(respuesta.status_code, 200)
