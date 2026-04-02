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

    def clean(self):
        super().clean()
        if self.estado in ['CONCLUIDA', 'TITULADA'] and self.pk:
            # Validacion comite tutorial
            if self.programa.nivel in ['MAESTRIA', 'DOCTORADO', 'DOCTORADO_DIRECTO']:
                num_comite = self.comite_tutorial.filter(activo=True).count()
                if num_comite < 3:
                    raise ValidationError({'estado': 'El comite tutorial requiere minimo 3 integrantes para estar activa/concluida.'})
            # Validacion directores
            num_dir = self.directores.filter(activo=True).count()
            if num_dir < 1 or num_dir > 2:
                raise ValidationError({'estado': 'La tesis debe tener 1 o 2 directores activos.'})


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
        super().clean()
        if self.tesis and self.activo:
            directores_actuales = DirectorTesis.objects.filter(
                tesis=self.tesis,
                activo=True
            ).exclude(pk=self.pk).count()
            if directores_actuales >= 2:
                raise ValidationError('Una tesis no puede tener mas de 2 directores activos (Articulo 19).')
            
            # grado igual o superior
            niveles = {'MAESTRIA': 1, 'DOCTORADO': 2, 'DOCTORADO_DIRECTO': 2}
            grados_profesor = {'LICENCIATURA': 0, 'MAESTRIA': 1, 'DOCTORADO': 2}
            nivel_tesis_val = niveles.get(self.tesis.programa.nivel, 0)
            grado_prof_val = grados_profesor.get(self.profesor.grado_academico, 0)
            
            if grado_prof_val < nivel_tesis_val:
                raise ValidationError('El director debe tener un grado academico igual o superior al nivel de la tesis.')

            # Nombramiento Profesor de Posgrado activo
            from apps.nombramientos.models import Nombramiento
            t_nombramientos = Nombramiento.objects.filter(
                profesor=self.profesor,
                tipo__nombramiento='Profesor de Posgrado',
                tipo__origen='IPN'
            )
            has_vigente = any(n.esta_vigente for n in t_nombramientos)
            if not has_vigente:
                raise ValidationError('El director debe tener un Nombramiento de Profesor de Posgrado vigente emitido por el IPN.')


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
        super().clean()
        if self.tesis:
            programa = self.tesis.programa
            if programa.nivel not in ['MAESTRIA', 'DOCTORADO', 'DOCTORADO_DIRECTO']:
                raise ValidationError('El comite tutorial solo aplica a programas de Maestria, Doctorado o Doctorado Directo.')


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

    def clean(self):
        super().clean()
        if self.profesor.grado_academico != 'DOCTORADO':
            raise ValidationError('Todos los sinodales deben tener grado de Doctor (Art. 30).')

        qs_titulares = JuradoExamen.objects.filter(
            estudiante=self.estudiante, tipo_examen=self.tipo_examen, rol__in=['PRESIDENTE', 'SECRETARIO', 'VOCAL']
        )
        qs_suplentes = JuradoExamen.objects.filter(
            estudiante=self.estudiante, tipo_examen=self.tipo_examen, rol='SUPLENTE'
        )
        if self.pk:
            qs_titulares = qs_titulares.exclude(pk=self.pk)
            qs_suplentes = qs_suplentes.exclude(pk=self.pk)

        if self.rol in ['PRESIDENTE', 'SECRETARIO', 'VOCAL'] and qs_titulares.count() >= 5:
            raise ValidationError('El jurado de examen de grado requiere exactamente 5 sinodales titulares.')
        if self.rol == 'SUPLENTE' and qs_suplentes.count() >= 1:
            raise ValidationError('El jurado de examen de grado requiere exactamente 1 suplente.')
