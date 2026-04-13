import re
import unicodedata
from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class ModeloBase(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def normalizar_texto(texto):
    nfkd = unicodedata.normalize('NFKD', texto)
    sin_tildes = ''.join(c for c in nfkd if not unicodedata.combining(c))
    return sin_tildes.upper().strip()


class Persona(ModeloBase):
    paterno = models.CharField(max_length=45)
    materno = models.CharField(max_length=45, blank=True)
    nombres = models.CharField(max_length=45)
    rfc = models.CharField(max_length=13, unique=True, blank=True, null=True)
    curp = models.CharField(max_length=18, unique=True, blank=True, null=True)
    cvu = models.CharField(max_length=10, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    genero = models.CharField(
        max_length=2,
        choices=[('M', 'Masculino'), ('F', 'Femenino'), ('NB', 'No binario'), ('NE', 'No especificado')],
        blank=True
    )
    fecha_nacimiento = models.DateField(blank=True, null=True)
    foto = models.ImageField(upload_to='personas/fotos/', blank=True, null=True)
    usuario = models.OneToOneField('cuentas.Usuario', on_delete=models.SET_NULL, null=True, blank=True, related_name='persona')

    class Meta:
        verbose_name = 'persona'
        verbose_name_plural = 'personas'
        ordering = ['paterno', 'materno', 'nombres']

    def __str__(self):
        return f'{self.paterno} {self.materno}, {self.nombres}'

    @property
    def nombre_completo(self):
        return f'{self.nombres} {self.paterno} {self.materno}'.strip()

    def clean(self):
        super().clean()
        errores = {}
        self._validar_fecha_nacimiento(errores)
        self._validar_curp_fecha(errores)
        self._validar_curp_genero(errores)
        self._validar_curp_paterno(errores)
        self._validar_curp_materno(errores)
        self._validar_rfc_fecha(errores)
        self._validar_consistencia_curp_rfc(errores)
        if errores:
            raise ValidationError(errores)

    def _validar_fecha_nacimiento(self, errores):
        if not self.fecha_nacimiento:
            return
        hoy = date.today()
        if self.fecha_nacimiento > hoy:
            errores['fecha_nacimiento'] = 'La fecha de nacimiento no puede ser una fecha futura.'
        if self.fecha_nacimiento < date(1900, 1, 1):
            errores['fecha_nacimiento'] = 'La fecha de nacimiento no puede ser anterior al 1 de enero de 1900.'

    def _validar_curp_fecha(self, errores):
        if not self.curp or not self.fecha_nacimiento or len(self.curp) < 10:
            return
        fecha_curp = self.curp[4:10]
        fecha_esperada = self.fecha_nacimiento.strftime('%y%m%d')
        if fecha_curp != fecha_esperada:
            errores['curp'] = (
                f'La fecha en la CURP ({fecha_curp}) no coincide con la fecha de nacimiento '
                f'registrada ({fecha_esperada}).'
            )

    def _validar_curp_genero(self, errores):
        if not self.curp or not self.genero or len(self.curp) < 11:
            return
        sexo_curp = self.curp[10]
        correspondencia = {'M': 'H', 'F': 'M'}
        esperado = correspondencia.get(self.genero)
        if esperado and sexo_curp != esperado:
            errores['genero'] = (
                f'El genero registrado ({self.genero}) no corresponde con el sexo '
                f'indicado en la CURP ({sexo_curp}).'
            )

    def _validar_curp_paterno(self, errores):
        if not self.curp or not self.paterno or len(self.curp) < 1:
            return
        inicial_paterno = normalizar_texto(self.paterno)[0] if self.paterno.strip() else ''
        if inicial_paterno and self.curp[0] != inicial_paterno:
            errores['paterno'] = (
                f'La primera letra del apellido paterno ({inicial_paterno}) no coincide '
                f'con la posicion 0 de la CURP ({self.curp[0]}).'
            )

    def _validar_curp_materno(self, errores):
        if not self.curp or len(self.curp) < 3:
            return
        if self.materno and self.materno.strip():
            inicial_materno = normalizar_texto(self.materno)[0]
            if self.curp[2] != inicial_materno:
                errores['materno'] = (
                    f'La primera letra del apellido materno ({inicial_materno}) no coincide '
                    f'con la posicion 2 de la CURP ({self.curp[2]}).'
                )
        else:
            if self.curp[2] != 'X':
                errores['materno'] = (
                    'Sin apellido materno registrado, la posicion 2 de la CURP debe ser X.'
                )

    def _validar_rfc_fecha(self, errores):
        if not self.rfc or len(self.rfc) != 13 or not self.fecha_nacimiento:
            return
        fecha_rfc = self.rfc[4:10]
        fecha_esperada = self.fecha_nacimiento.strftime('%y%m%d')
        if fecha_rfc != fecha_esperada:
            errores['rfc'] = (
                f'La fecha en el RFC ({fecha_rfc}) no coincide con la fecha de nacimiento '
                f'registrada ({fecha_esperada}).'
            )

    def _validar_consistencia_curp_rfc(self, errores):
        if not self.curp or not self.rfc or len(self.curp) < 10 or len(self.rfc) != 13:
            return
        if 'rfc' in errores:
            return
        if self.curp[4:10] != self.rfc[4:10]:
            errores['rfc'] = (
                f'La fecha codificada en la CURP ({self.curp[4:10]}) no coincide '
                f'con la del RFC ({self.rfc[4:10]}).'
            )


class Profesor(ModeloBase):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='profesor')
    grado_academico = models.CharField(
        max_length=20,
        choices=[('LICENCIATURA', 'Licenciatura'), ('MAESTRIA', 'Maestria'), ('DOCTORADO', 'Doctorado')]
    )
    laboratorio = models.ForeignKey(
        'programas.Laboratorio', on_delete=models.SET_NULL, null=True, blank=True, related_name='profesores'
    )
    numero_empleado = models.CharField(max_length=20, unique=True, blank=True, null=True)
    departamento = models.CharField(max_length=100, blank=True)
    orcid = models.CharField(max_length=25, unique=True, blank=True, null=True, verbose_name='ORCID')
    fecha_ingreso_ipn = models.DateField(blank=True, null=True)
    fecha_ingreso_cic = models.DateField(blank=True, null=True)
    es_externo = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'profesor'
        verbose_name_plural = 'profesores'
        ordering = ['persona__paterno']

    def __str__(self):
        return str(self.persona)

    def total_alumnos_activos(self):
        return self.direcciones_tesis.filter(activo=True).count()

    def puede_dirigir_mas_alumnos(self):
        return self.total_alumnos_activos() < 4

    def clean(self):
        super().clean()
        errores = {}
        self._validar_fechas_ingreso(errores)
        self._validar_externo_laboratorio(errores)
        if errores:
            raise ValidationError(errores)

    def _validar_fechas_ingreso(self, errores):
        hoy = date.today()
        if self.fecha_ingreso_ipn and self.fecha_ingreso_ipn > hoy:
            errores['fecha_ingreso_ipn'] = 'La fecha de ingreso al IPN no puede ser futura.'
        if self.fecha_ingreso_cic and self.fecha_ingreso_cic > hoy:
            errores['fecha_ingreso_cic'] = 'La fecha de ingreso al CIC no puede ser futura.'
        if self.fecha_ingreso_cic and self.fecha_ingreso_ipn:
            if self.fecha_ingreso_cic < self.fecha_ingreso_ipn:
                errores['fecha_ingreso_cic'] = (
                    'La fecha de ingreso al CIC no puede ser anterior a la fecha de ingreso al IPN.'
                )

    def _validar_externo_laboratorio(self, errores):
        if self.es_externo and self.laboratorio_id:
            errores['laboratorio'] = (
                'Un investigador externo al CIC no puede tener laboratorio del CIC asignado.'
            )


class Estudiante(ModeloBase):
    class Estado(models.TextChoices):
        ACTIVO = 'ACTIVO', 'Activo'
        EGRESADO = 'EGRESADO', 'Egresado'
        BAJA_TEMPORAL = 'BAJA_TEMPORAL', 'Baja temporal'
        BAJA_DEFINITIVA = 'BAJA_DEFINITIVA', 'Baja definitiva'
        GRADUADO = 'GRADUADO', 'Graduado'

    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='estudiante')
    matricula = models.CharField(max_length=10, unique=True)
    programa = models.ForeignKey('programas.Programa', on_delete=models.PROTECT, related_name='estudiantes')
    generacion = models.IntegerField()
    modalidad = models.CharField(max_length=2, choices=[('TC', 'Tiempo completo'), ('TP', 'Tiempo parcial')], default='TC')
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ACTIVO)
    fecha_ingreso = models.DateField()
    fecha_egreso = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'alumno'
        verbose_name_plural = 'alumnos'
        ordering = ['matricula']

    def __str__(self):
        return f'{self.matricula} — {self.persona}'

    def clean(self):
        super().clean()
        errores = {}
        self._validar_fechas(errores)
        self._validar_estado_fecha_egreso(errores)
        self._validar_generacion(errores)
        self._validar_modalidad_nivel(errores)
        self._validar_plazo_maximo(errores)
        if errores:
            raise ValidationError(errores)

    def _validar_fechas(self, errores):
        hoy = date.today()
        if self.fecha_ingreso and self.fecha_ingreso > hoy:
            errores['fecha_ingreso'] = 'La fecha de ingreso no puede ser futura.'
        if self.fecha_ingreso and self.fecha_egreso:
            if self.fecha_egreso <= self.fecha_ingreso:
                errores['fecha_egreso'] = 'La fecha de egreso debe ser posterior a la fecha de ingreso.'

    def _validar_estado_fecha_egreso(self, errores):
        estados_con_egreso = {'EGRESADO', 'GRADUADO', 'BAJA_DEFINITIVA'}
        if self.estado in estados_con_egreso and not self.fecha_egreso:
            errores['fecha_egreso'] = (
                f'Un estudiante con estado {self.get_estado_display()} debe tener fecha de egreso.'
            )
        if self.estado == 'ACTIVO' and self.fecha_egreso:
            errores['fecha_egreso'] = 'Un estudiante activo no puede tener fecha de egreso registrada.'

    def _validar_generacion(self, errores):
        if self.generacion and self.fecha_ingreso:
            if self.generacion != self.fecha_ingreso.year:
                errores['generacion'] = (
                    f'La generacion ({self.generacion}) debe coincidir con el anio '
                    f'de la fecha de ingreso ({self.fecha_ingreso.year}).'
                )

    def _validar_modalidad_nivel(self, errores):
        if not self.programa_id:
            return
        try:
            nivel = self.programa.nivel
        except Exception:
            return
        if nivel in ('DOCTORADO', 'DOCTORADO_DIRECTO') and self.modalidad == 'TP':
            errores['modalidad'] = (
                'Los programas de Doctorado del CIC son exclusivamente de tiempo completo (TC). '
                'Art. 13, Reglamento de Estudios de Posgrado IPN.'
            )

    def _validar_plazo_maximo(self, errores):
        if self.estado != 'ACTIVO' or not self.fecha_ingreso:
            return
        if not self.programa_id:
            return
        try:
            nivel = self.programa.nivel
        except Exception:
            return
        plazos = {
            ('MAESTRIA', 'TC'): 30,
            ('MAESTRIA', 'TP'): 42,
            ('DOCTORADO', 'TC'): 48,
            ('DOCTORADO_DIRECTO', 'TC'): 60,
        }
        plazo = plazos.get((nivel, self.modalidad))
        if not plazo:
            return
        hoy = date.today()
        meses_transcurridos = (hoy.year - self.fecha_ingreso.year) * 12 + (hoy.month - self.fecha_ingreso.month)
        if meses_transcurridos > plazo:
            errores['__all__'] = (
                f'ADVERTENCIA: El estudiante ha superado el plazo maximo de {plazo} meses '
                f'({meses_transcurridos} meses transcurridos). '
                f'Arts. 26/27, Reglamento de Estudios de Posgrado IPN.'
            )
