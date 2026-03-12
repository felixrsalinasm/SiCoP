from django.db import models
from django.core.exceptions import ValidationError
from apps.personas.models import ModeloBase

class DirectorTesis(ModeloBase):
    estudiante = models.ForeignKey('personas.Estudiante', on_delete=models.CASCADE, related_name='direcciones_recibidas')
    profesor = models.ForeignKey('personas.Profesor', on_delete=models.CASCADE, related_name='direcciones_tesis')
    es_codirector = models.BooleanField(default=False)
    fecha_asignacion = models.DateField()
    fecha_termino = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'director de tesis'
        verbose_name_plural = 'directores de tesis'
        unique_together = ('estudiante', 'profesor')

    def __str__(self):
        rol = 'Codirector' if self.es_codirector else 'Director'
        return f'{rol}: {self.profesor} → {self.estudiante}'

    def clean(self):
        if self.activo:
            directores_actuales = DirectorTesis.objects.filter(
                estudiante=self.estudiante,
                activo=True
            ).exclude(pk=self.pk).count()
            if directores_actuales >= 2:
                raise ValidationError('Un estudiante no puede tener más de 2 directores de tesis activos (Artículo 19, Reglamento IPN).')
            if not self.profesor.puede_dirigir_mas_alumnos():
                raise ValidationError('Este profesor ya tiene 4 alumnos activos como director de tesis (política interna CIC).')

class ComiteTutorial(ModeloBase):
    estudiante = models.ForeignKey('personas.Estudiante', on_delete=models.CASCADE, related_name='comite_tutorial')
    profesor = models.ForeignKey('personas.Profesor', on_delete=models.CASCADE, related_name='comites_tutoriales')
    fecha_asignacion = models.DateField()
    fecha_termino = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'comité tutorial'
        verbose_name_plural = 'comités tutoriales'
        unique_together = ('estudiante', 'profesor')

    def __str__(self):
        return f'Comité: {self.profesor} → {self.estudiante}'

class JuradoExamen(ModeloBase):
    class TipoExamen(models.TextChoices):
        GRADO = 'GRADO', 'Examen de grado'
        PREDOCTORAL = 'PREDOCTORAL', 'Examen predoctoral'

    class RolJurado(models.TextChoices):
        PRESIDENTE = 'PRESIDENTE', 'Presidente'
        SECRETARIO = 'SECRETARIO', 'Secretario'
        VOCAL = 'VOCAL', 'Vocal'
        SUPLENTE = 'SUPLENTE', 'Suplente'

    class Resultado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        APROBADO = 'APROBADO', 'Aprobado'
        NO_APROBADO = 'NO_APROBADO', 'No aprobado'

    estudiante = models.ForeignKey('personas.Estudiante', on_delete=models.CASCADE, related_name='jurados')
    profesor = models.ForeignKey('personas.Profesor', on_delete=models.CASCADE, related_name='participaciones_jurado')
    tipo_examen = models.CharField(max_length=15, choices=TipoExamen.choices)
    rol = models.CharField(max_length=15, choices=RolJurado.choices)
    fecha_examen = models.DateField(blank=True, null=True)
    resultado = models.CharField(max_length=15, choices=Resultado.choices, default=Resultado.PENDIENTE)

    class Meta:
        verbose_name = 'jurado de examen'
        verbose_name_plural = 'jurados de examen'
        unique_together = ('estudiante', 'profesor', 'tipo_examen')

    def __str__(self):
        return f'{self.get_rol_display()}: {self.profesor} — {self.estudiante} ({self.get_tipo_examen_display()})'
