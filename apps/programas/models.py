from django.db import models
from apps.personas.models import ModeloBase

class Laboratorio(ModeloBase):
    nombre = models.CharField(max_length=100)
    siglas = models.CharField(max_length=20, unique=True)
    jefe = models.ForeignKey('personas.Profesor', on_delete=models.SET_NULL, null=True, blank=True, related_name='laboratorios_dirigidos')

    class Meta:
        verbose_name = 'laboratorio'
        verbose_name_plural = 'laboratorios'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.siglas} — {self.nombre}'

class Programa(ModeloBase):
    class Nivel(models.TextChoices):
        MAESTRIA = 'MAESTRIA', 'Maestría'
        DOCTORADO = 'DOCTORADO', 'Doctorado'
        ESPECIALIDAD = 'ESPECIALIDAD', 'Especialidad'

    nombre = models.CharField(max_length=100)
    siglas = models.CharField(max_length=10, unique=True)
    nivel = models.CharField(max_length=15, choices=Nivel.choices)
    url_doc_base = models.URLField(blank=True)
    fecha_creacion = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'programa'
        verbose_name_plural = 'programas'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.siglas} — {self.nombre}'

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
