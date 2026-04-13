from datetime import date

from django.core.exceptions import ValidationError
from django.db import models

from apps.personas.models import ModeloBase


class Laboratorio(ModeloBase):
    nombre = models.CharField(max_length=100)
    siglas = models.CharField(max_length=20, unique=True)
    jefe = models.ForeignKey(
        'personas.Profesor', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='laboratorios_dirigidos'
    )

    class Meta:
        verbose_name = 'laboratorio'
        verbose_name_plural = 'laboratorios'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.siglas} — {self.nombre}'


class Programa(ModeloBase):
    class Nivel(models.TextChoices):
        ESPECIALIDAD = 'ESPECIALIDAD', 'Especialidad'
        MAESTRIA = 'MAESTRIA', 'Maestria'
        DOCTORADO = 'DOCTORADO', 'Doctorado'
        DOCTORADO_DIRECTO = 'DOCTORADO_DIRECTO', 'Doctorado Directo'

    DURACION_MAXIMA = {
        'MAESTRIA': 30,
        'DOCTORADO': 48,
        'DOCTORADO_DIRECTO': 60,
    }

    nombre = models.CharField(max_length=100)
    siglas = models.CharField(max_length=10, unique=True)
    nivel = models.CharField(max_length=20, choices=Nivel.choices)
    duracion_maxima_meses = models.PositiveIntegerField(blank=True, null=True)
    url_doc_base = models.URLField(blank=True)
    fecha_creacion = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'programa'
        verbose_name_plural = 'programas'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.siglas} — {self.nombre}'

    def clean(self):
        tope = self.DURACION_MAXIMA.get(self.nivel)
        if tope and self.duracion_maxima_meses and self.duracion_maxima_meses > tope:
            raise ValidationError(
                f'La duracion maxima para {self.get_nivel_display()} no puede exceder {tope} meses.'
            )

    def save(self, *args, **kwargs):
        if not self.duracion_maxima_meses:
            self.duracion_maxima_meses = self.DURACION_MAXIMA.get(self.nivel)
        super().save(*args, **kwargs)


class Coordinador(ModeloBase):
    profesor = models.ForeignKey('personas.Profesor', on_delete=models.PROTECT, related_name='coordinaciones')
    programa = models.ForeignKey(Programa, on_delete=models.PROTECT, related_name='coordinadores')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'coordinador'
        verbose_name_plural = 'coordinadores'
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f'{self.profesor} — {self.programa.siglas}'

    def es_actual(self):
        return self.fecha_fin is None

    def clean(self):
        super().clean()
        errores = {}
        self._validar_fechas(errores)
        self._validar_unicidad_coordinador_activo(errores)
        if errores:
            raise ValidationError(errores)

    def _validar_fechas(self, errores):
        hoy = date.today()
        if self.fecha_inicio and self.fecha_inicio > hoy:
            errores['fecha_inicio'] = 'La fecha de inicio no puede ser futura.'
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_fin <= self.fecha_inicio:
                errores['fecha_fin'] = (
                    'La fecha de fin debe ser posterior a la fecha de inicio.'
                )

    def _validar_unicidad_coordinador_activo(self, errores):
        if self.fecha_fin is not None or not self.programa_id:
            return
        qs = Coordinador.objects.filter(
            programa=self.programa, fecha_fin__isnull=True
        ).exclude(pk=self.pk)
        coordinador_activo = qs.first()
        if coordinador_activo:
            errores['programa'] = (
                f'Ya existe un coordinador activo para este programa: '
                f'{coordinador_activo.profesor}.'
            )
