from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
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
            if self.programa.nivel in ['MAESTRIA', 'DOCTORADO', 'DOCTORADO_DIRECTO']:
                num_comite = self.comite_tutorial.filter(activo=True).count()
                if num_comite < 3:
                    raise ValidationError({
                        'estado': 'El comite tutorial requiere minimo 3 integrantes para concluir la tesis.'
                    })
            num_dir = self.directores.filter(activo=True).count()
            if num_dir < 1 or num_dir > 2:
                raise ValidationError({
                    'estado': 'La tesis debe tener 1 o 2 directores activos.'
                })


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
        errores = {}
        self._validar_max_directores(errores)
        self._validar_max_alumnos(errores)
        self._validar_fechas(errores)
        self._validar_activo_fecha_termino(errores)
        self._validar_directores_externos(errores)
        self._validar_grado_director_doctorado(errores)
        self._validar_nombramiento_vigente(errores)
        if errores:
            raise ValidationError(errores)

    def _obtener_estudiante(self):
        if self.estudiante_id:
            return self.estudiante
        if self.tesis_id:
            try:
                return self.tesis.alumno
            except Exception:
                pass
        return None

    def _validar_max_directores(self, errores):
        if not self.tesis_id or not self.activo:
            return
        directores_actuales = DirectorTesis.objects.filter(
            tesis=self.tesis, activo=True
        ).exclude(pk=self.pk).count()
        if directores_actuales >= 2:
            errores['__all__'] = (
                'Una tesis no puede tener mas de 2 directores activos. '
                'Art. 19, Reglamento de Estudios de Posgrado IPN.'
            )

    def _validar_max_alumnos(self, errores):
        if not self.activo or not self.profesor_id:
            return
        try:
            if not self.profesor.puede_dirigir_mas_alumnos():
                existente = DirectorTesis.objects.filter(
                    profesor=self.profesor, activo=True, pk=self.pk
                ).exists()
                if not existente:
                    errores['profesor'] = (
                        'Este profesor ya tiene 4 alumnos activos como director de tesis.'
                    )
        except Exception:
            pass

    def _validar_fechas(self, errores):
        if self.fecha_termino and self.fecha_asignacion:
            if self.fecha_termino <= self.fecha_asignacion:
                errores['fecha_termino'] = (
                    'La fecha de termino debe ser posterior a la fecha de asignacion.'
                )
        estudiante = self._obtener_estudiante()
        if estudiante and self.fecha_asignacion and estudiante.fecha_ingreso:
            if self.fecha_asignacion < estudiante.fecha_ingreso:
                errores['fecha_asignacion'] = (
                    'La fecha de asignacion no puede ser anterior a la fecha de ingreso del estudiante.'
                )

    def _validar_activo_fecha_termino(self, errores):
        if self.activo and self.fecha_termino:
            errores['fecha_termino'] = (
                'Un director activo no debe tener fecha de termino registrada.'
            )
        if not self.activo and not self.fecha_termino:
            errores['fecha_termino'] = (
                'Un director inactivo debe tener fecha de termino registrada.'
            )

    def _validar_directores_externos(self, errores):
        if not self.activo or not self.tesis_id or not self.profesor_id:
            return
        try:
            es_externo = self.profesor.es_externo
        except Exception:
            return
        if not es_externo:
            return
        otro_externo = DirectorTesis.objects.filter(
            tesis=self.tesis, activo=True, profesor__es_externo=True
        ).exclude(pk=self.pk).exists()
        if otro_externo:
            errores['profesor'] = (
                'No pueden haber 2 directores externos simultaneos para la misma tesis. '
                'Art. 19, Reglamento de Estudios de Posgrado IPN.'
            )

    def _validar_grado_director_doctorado(self, errores):
        if not self.tesis_id or not self.profesor_id or not self.activo:
            return
        try:
            nivel = self.tesis.programa.nivel
            grado = self.profesor.grado_academico
        except Exception:
            return
        if nivel in ('DOCTORADO', 'DOCTORADO_DIRECTO') and grado != 'DOCTORADO':
            errores.setdefault('__all__', '')
            if errores['__all__']:
                errores['__all__'] += ' '
            errores['__all__'] += (
                'ADVERTENCIA: Para dirigir tesis de Doctorado, el director debe tener '
                'grado de Doctor. Art. 19, Reglamento de Estudios de Posgrado IPN.'
            )

    def _validar_nombramiento_vigente(self, errores):
        if not self.activo or not self.profesor_id:
            return
        try:
            es_externo = self.profesor.es_externo
        except Exception:
            return
        if es_externo:
            return
        from apps.nombramientos.models import Nombramiento
        nombramientos = Nombramiento.objects.filter(
            profesor=self.profesor,
            tipo__nombramiento__icontains='Profesor de Posgrado'
        )
        tiene_vigente = any(n.vigente for n in nombramientos)
        if not tiene_vigente:
            errores.setdefault('__all__', '')
            if errores['__all__']:
                errores['__all__'] += ' '
            errores['__all__'] += (
                'ADVERTENCIA: El director interno debe tener un Nombramiento vigente de '
                'Profesor de Posgrado. Art. 19, Reglamento de Estudios de Posgrado IPN.'
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
        super().clean()
        errores = {}
        self._validar_nivel_programa(errores)
        self._validar_fechas(errores)
        self._validar_activo_fecha_termino(errores)
        if errores:
            raise ValidationError(errores)

    def _obtener_nivel(self):
        if self.tesis_id:
            try:
                return self.tesis.programa.nivel
            except Exception:
                pass
        if self.estudiante_id:
            try:
                return self.estudiante.programa.nivel
            except Exception:
                pass
        return None

    def _validar_nivel_programa(self, errores):
        nivel = self._obtener_nivel()
        if not nivel:
            return
        if nivel == 'ESPECIALIDAD':
            errores['__all__'] = (
                'Los programas de Especialidad no requieren Comite Tutorial. '
                'Art. 22, Reglamento de Estudios de Posgrado IPN.'
            )
        elif nivel not in ('MAESTRIA', 'DOCTORADO', 'DOCTORADO_DIRECTO'):
            errores['__all__'] = (
                'El comite tutorial solo aplica a programas de Maestria, Doctorado o Doctorado Directo.'
            )

    def _validar_fechas(self, errores):
        if self.fecha_termino and self.fecha_asignacion:
            if self.fecha_termino <= self.fecha_asignacion:
                errores['fecha_termino'] = (
                    'La fecha de termino debe ser posterior a la fecha de asignacion.'
                )

    def _validar_activo_fecha_termino(self, errores):
        if self.activo and self.fecha_termino:
            errores['fecha_termino'] = (
                'Un miembro activo del comite no debe tener fecha de termino registrada.'
            )
        if not self.activo and not self.fecha_termino:
            errores['fecha_termino'] = (
                'Un miembro inactivo del comite debe tener fecha de termino registrada.'
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

    def clean(self):
        super().clean()
        errores = {}
        self._validar_max_titulares_suplentes(errores)
        self._validar_grado_doctor(errores)
        self._validar_resultado_fecha(errores)
        self._validar_tipo_examen_nivel(errores)
        if errores:
            raise ValidationError(errores)

    def _validar_max_titulares_suplentes(self, errores):
        if not self.estudiante_id:
            return
        qs_titulares = JuradoExamen.objects.filter(
            estudiante=self.estudiante,
            tipo_examen=self.tipo_examen,
            rol__in=['PRESIDENTE', 'SECRETARIO', 'VOCAL']
        )
        qs_suplentes = JuradoExamen.objects.filter(
            estudiante=self.estudiante,
            tipo_examen=self.tipo_examen,
            rol='SUPLENTE'
        )
        if self.pk:
            qs_titulares = qs_titulares.exclude(pk=self.pk)
            qs_suplentes = qs_suplentes.exclude(pk=self.pk)

        if self.rol in ('PRESIDENTE', 'SECRETARIO', 'VOCAL') and qs_titulares.count() >= 5:
            errores['rol'] = (
                'El jurado de examen requiere maximo 5 sinodales titulares. '
                'Art. 30, Reglamento de Estudios de Posgrado IPN.'
            )
        if self.rol == 'SUPLENTE' and qs_suplentes.count() >= 1:
            errores['rol'] = (
                'El jurado de examen requiere maximo 1 suplente. '
                'Art. 30, Reglamento de Estudios de Posgrado IPN.'
            )

    def _validar_grado_doctor(self, errores):
        if not self.profesor_id:
            return
        try:
            grado = self.profesor.grado_academico
        except Exception:
            return
        if grado != 'DOCTORADO':
            nivel = None
            if self.estudiante_id:
                try:
                    nivel = self.estudiante.programa.nivel
                except Exception:
                    pass
            if nivel in ('DOCTORADO', 'DOCTORADO_DIRECTO'):
                errores.setdefault('__all__', '')
                if errores['__all__']:
                    errores['__all__'] += ' '
                errores['__all__'] += (
                    'ADVERTENCIA: Todos los sinodales deben tener grado de Doctor. '
                    'Art. 30, Reglamento de Estudios de Posgrado IPN.'
                )
            else:
                errores['profesor'] = (
                    'Todos los sinodales deben tener grado de Doctor. '
                    'Art. 30, Reglamento de Estudios de Posgrado IPN.'
                )

    def _validar_resultado_fecha(self, errores):
        if self.resultado in ('APROBADO', 'NO_APROBADO') and not self.fecha_examen:
            errores['fecha_examen'] = (
                'La fecha de examen es obligatoria cuando el resultado ha sido registrado.'
            )
        if self.resultado == 'PENDIENTE' and self.fecha_examen:
            hoy = date.today()
            if self.fecha_examen < hoy:
                errores.setdefault('__all__', '')
                if errores['__all__']:
                    errores['__all__'] += ' '
                errores['__all__'] += (
                    'ADVERTENCIA: El resultado sigue en PENDIENTE pero la fecha de examen ya paso.'
                )

    def _validar_tipo_examen_nivel(self, errores):
        if self.tipo_examen != 'PREDOCTORAL' or not self.estudiante_id:
            return
        try:
            nivel = self.estudiante.programa.nivel
        except Exception:
            return
        if nivel not in ('DOCTORADO', 'DOCTORADO_DIRECTO'):
            errores['tipo_examen'] = (
                'El examen predoctoral solo aplica a estudiantes de Doctorado. '
                'Art. 25, Reglamento de Estudios de Posgrado IPN.'
            )
