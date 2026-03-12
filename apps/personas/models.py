from django.db import models

class ModeloBase(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Persona(ModeloBase):
    paterno = models.CharField(max_length=45)
    materno = models.CharField(max_length=45, blank=True)
    nombres = models.CharField(max_length=45)
    rfc = models.CharField(max_length=13, unique=True, blank=True, null=True)
    curp = models.CharField(max_length=18, unique=True, blank=True, null=True)
    cvu = models.CharField(max_length=10, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    genero = models.CharField(max_length=2, choices=[('M','Masculino'),('F','Femenino'),('NB','No binario'),('NE','No especificado')], blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    foto = models.ImageField(upload_to='personas/fotos/', blank=True, null=True)
    usuario = models.OneToOneField('cuentas.Usuario', on_delete=models.SET_NULL, null=True, blank=True, related_name='persona')

    class Meta:
        verbose_name = 'persona'
        verbose_name_plural = 'personas'
        ordering = ['paterno', 'materno', 'nombres']

    def __str__(self):
        return f'{self.paterno} {self.materno}, {self.nombres}'

    def nombre_completo(self):
        return f'{self.nombres} {self.paterno} {self.materno}'.strip()

class Profesor(ModeloBase):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='profesor')
    grado_academico = models.CharField(max_length=20, choices=[('LICENCIATURA','Licenciatura'),('MAESTRIA','Maestría'),('DOCTORADO','Doctorado')])
    laboratorio = models.ForeignKey('programas.Laboratorio', on_delete=models.SET_NULL, null=True, blank=True, related_name='profesores')
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
    modalidad = models.CharField(max_length=2, choices=[('TC','Tiempo completo'),('TP','Tiempo parcial')], default='TC')
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ACTIVO)
    fecha_ingreso = models.DateField()
    fecha_egreso = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'estudiante'
        verbose_name_plural = 'estudiantes'
        ordering = ['matricula']

    def __str__(self):
        return f'{self.matricula} — {self.persona}'
