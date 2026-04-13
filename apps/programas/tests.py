from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.personas.models import Persona, Profesor
from apps.programas.models import Programa, Coordinador


class TestCoordinadorValidaciones(TestCase):
    def setUp(self):
        self.programa = Programa.objects.create(
            siglas='MCC_C', nombre='Maestria Coord', nivel='MAESTRIA', activo=True
        )
        persona1 = Persona.objects.create(
            paterno='Coord', materno='Uno', nombres='Prof', email='coord1@ipn.mx'
        )
        self.prof1 = Profesor.objects.create(
            persona=persona1, grado_academico='DOCTORADO', activo=True
        )
        persona2 = Persona.objects.create(
            paterno='Coord', materno='Dos', nombres='Prof', email='coord2@ipn.mx'
        )
        self.prof2 = Profesor.objects.create(
            persona=persona2, grado_academico='DOCTORADO', activo=True
        )

    def test_segundo_coordinador_activo_rechazado(self):
        Coordinador.objects.create(
            profesor=self.prof1, programa=self.programa,
            fecha_inicio=date(2023, 1, 1)
        )
        coord2 = Coordinador(
            profesor=self.prof2, programa=self.programa,
            fecha_inicio=date(2024, 1, 1)
        )
        with self.assertRaises(ValidationError) as ctx:
            coord2.clean()
        self.assertIn('programa', ctx.exception.message_dict)

    def test_fecha_fin_anterior_a_inicio_rechazada(self):
        coord = Coordinador(
            profesor=self.prof1, programa=self.programa,
            fecha_inicio=date(2024, 1, 1), fecha_fin=date(2023, 6, 1)
        )
        with self.assertRaises(ValidationError) as ctx:
            coord.clean()
        self.assertIn('fecha_fin', ctx.exception.message_dict)
