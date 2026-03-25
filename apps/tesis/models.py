from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.personas.models import ModeloBase


class Tesis(ModeloBase):
    class EstadoTesis(models.TextChoices):
        EN_PROCESO = 'EN_PROCESO', 'En proceso'
        CONCLUIDA = 'CONCLUIDA', 'Concluida'
        TITULADA = 'TITULADA', 'Titulada'

    titulo = models.CharField(max_length=255)
    resumen = models.TextField(blank=True)
    estado = models.CharField(max_length=15, choices=EstadoTesis.choices, default=EstadoTesis.EN_PROCESO)
    fecha_registro = models.DateField()
    alumno = models.ForeignKey('personas.Estudiante', on_delete=models.CASCADE, related_name='tesis')
    programa = models.ForeignKey('programas.Programa', on_delete=models.PROTECT, related_name='tesis')

    class Meta:
        verbose_name = 'tesis'
        verbose_name_plural = 'tesis'
        ordering = ['-fecha_registro']

    def __str__(self):
        return self.titulo


class DirectorTesis(ModeloBase):
    class TipoDireccion(models.TextChoices):
        DIRECTOR = 'DIRECTOR', 'Director'
        CODIRECTOR = 'CODIRECTOR', 'Codirector'

    tesis = models.ForeignKey(Tesis, on_delete=models.CASCADE, related_name='directores', null=True, blank=True)
    estudiante = models.ForeignKey(
        'personas.Estudiante', on_delete=models.CASCADE, related_name='direcciones_recibidas',
        null=True, blank=True
    )
    profesor = models.ForeignKey('personas.Profesor', on_delete=models.CASCADE, related_name='direcciones_tesis')
    tipo_direccion = models.CharField(
        max_length=15, choices=TipoDireccion.choices, default=TipoDireccion.DIRECTOR
    )
    es_codirector = models.BooleanField(default=False)
    fecha_asignacion = models.DateField()
    fecha_termino = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'director de tesis'
        verbose_name_plural = 'directores de tesis'
        unique_together = ('tesis', 'profesor')

    def __str__(self):
        return f'{self.get_tipo_direccion_display()}: {self.profesor} -> {self.tesis}'

    def clean(self):
        if self.tesis and self.activo:
            directores_actuales = DirectorTesis.objects.filter(
                tesis=self.tesis,
                activo=True
            ).exclude(pk=self.pk).count()
            if directores_actuales >= 2:
                raise ValidationError(
                    'Una tesis no puede tener mas de 2 directores activos (Articulo 19, Reglamento IPN).'
                )
            if not self.profesor.puede_dirigir_mas_alumnos():
                raise ValidationError(
                    'Este profesor ya tiene 4 alumnos activos como director de tesis.'
                )


class ComiteTutorial(ModeloBase):
    tesis = models.ForeignKey(Tesis, on_delete=models.CASCADE, related_name='comite_tutorial', null=True, blank=True)
    estudiante = models.ForeignKey(
        'personas.Estudiante', on_delete=models.CASCADE, related_name='comite_tutorial',
        null=True, blank=True
    )
    profesor = models.ForeignKey('personas.Profesor', on_delete=models.CASCADE, related_name='comites_tutoriales')
    rol = models.CharField(max_length=50, blank=True)
    fecha_asignacion = models.DateField()
    fecha_termino = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'comite tutorial'
        verbose_name_plural = 'comites tutoriales'
        unique_together = ('tesis', 'profesor')

    def __str__(self):
        return f'Comite: {self.profesor} -> {self.tesis}'

    def clean(self):
        if self.tesis:
            programa = self.tesis.programa
            if programa.nivel not in ['MAESTRIA', 'DOCTORADO', 'DOCTORADO_DIRECTO']:
                raise ValidationError(
                    'El comite tutorial solo aplica a programas de Maestria, Doctorado o Doctorado Directo.'
                )


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
