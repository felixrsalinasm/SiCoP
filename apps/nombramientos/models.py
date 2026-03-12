from django.db import models
from apps.personas.models import ModeloBase

class CatTipoNombramiento(ModeloBase):
    class Origen(models.TextChoices):
        IPN = 'IPN', 'IPN'
        CONAHCYT = 'CONAHCYT', 'CONAHCyT'
        EXTERNO = 'EXTERNO', 'Externo'

    nombramiento = models.CharField(max_length=60, unique=True)
    origen = models.CharField(max_length=10, choices=Origen.choices)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'tipo de nombramiento'
        verbose_name_plural = 'tipos de nombramiento'
        ordering = ['origen', 'nombramiento']

    def __str__(self):
        return f'{self.get_origen_display()} — {self.nombramiento}'

class Nombramiento(ModeloBase):
    clave = models.CharField(max_length=20, blank=True)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    tipo = models.ForeignKey(CatTipoNombramiento, on_delete=models.PROTECT, related_name='nombramientos')
    observaciones = models.TextField(blank=True)
    archivo = models.FileField(upload_to='nombramientos/', blank=True, null=True)

    class Meta:
        verbose_name = 'nombramiento'
        verbose_name_plural = 'nombramientos'
        ordering = ['-fecha_emision']

    def __str__(self):
        return f'{self.tipo} — {self.clave}'

    def esta_vigente(self):
        from django.utils import timezone
        return self.fecha_vencimiento >= timezone.now().date()

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
