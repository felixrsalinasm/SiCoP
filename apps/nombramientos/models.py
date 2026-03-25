from django.db import models
from django.utils import timezone
from apps.personas.models import ModeloBase


class CatTipoNombramiento(ModeloBase):
    class Origen(models.TextChoices):
        IPN = 'IPN', 'IPN'
        CONAHCYT = 'CONAHCYT', 'CONAHCyT'
        EXTERNO = 'EXTERNO', 'Externo'

    nombramiento = models.CharField(max_length=100, unique=True)
    origen = models.CharField(max_length=10, choices=Origen.choices, blank=True, default='IPN')
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'tipo de nombramiento'
        verbose_name_plural = 'tipos de nombramiento'
        ordering = ['nombramiento']

    def __str__(self):
        return self.nombramiento


class Nombramiento(ModeloBase):
    profesor = models.ForeignKey(
        'personas.Profesor', on_delete=models.CASCADE, related_name='nombramientos', null=True, blank=True
    )
    tipo = models.ForeignKey(CatTipoNombramiento, on_delete=models.PROTECT, related_name='nombramientos')
    clave = models.CharField(max_length=20, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    fecha_emision = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    archivo = models.FileField(upload_to='nombramientos/', blank=True, null=True)

    class Meta:
        verbose_name = 'nombramiento'
        verbose_name_plural = 'nombramientos'
        ordering = ['-fecha_inicio', '-fecha_emision']

    def __str__(self):
        prof = self.profesor if self.profesor else 'Sin profesor'
        return f'{self.tipo} — {prof}'

    @property
    def vigente(self):
        hoy = timezone.now().date()
        if self.fecha_fin:
            return self.fecha_fin >= hoy
        if self.fecha_vencimiento:
            return self.fecha_vencimiento >= hoy
        return True

    def esta_vigente(self):
        return self.vigente


class NombramientoProfesor(ModeloBase):
    profesor = models.ForeignKey('personas.Profesor', on_delete=models.CASCADE, related_name='nombramientos_profesor')
    nombramiento = models.ForeignKey(Nombramiento, on_delete=models.CASCADE, related_name='profesores_nombramiento')

    class Meta:
        verbose_name = 'nombramiento de profesor'
        verbose_name_plural = 'nombramientos de profesores'
        unique_together = ('profesor', 'nombramiento')

    def __str__(self):
        return f'{self.profesor} — {self.nombramiento}'


class ProgramaNombramiento(ModeloBase):
    programa = models.ForeignKey('programas.Programa', on_delete=models.CASCADE, related_name='nombramientos_programa')
    nombramiento = models.ForeignKey(Nombramiento, on_delete=models.CASCADE, related_name='programas_nombramiento')

    class Meta:
        verbose_name = 'nombramiento de programa'
        verbose_name_plural = 'nombramientos de programas'
        unique_together = ('programa', 'nombramiento')

    def __str__(self):
        return f'{self.programa} — {self.nombramiento}'
