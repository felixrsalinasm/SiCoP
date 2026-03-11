from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        COORDINADOR = 'COORDINADOR', 'Coordinador'
        SECRETARIA = 'SECRETARIA', 'Secretaria'
        PROFESOR = 'PROFESOR', 'Profesor'

    rol = models.CharField(max_length=20, choices=Roles.choices, default=Roles.SECRETARIA)

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def es_admin(self):
        return self.rol == self.Roles.ADMIN

    def es_coordinador(self):
        return self.rol == self.Roles.COORDINADOR

    def es_secretaria(self):
        return self.rol == self.Roles.SECRETARIA

    def es_profesor(self):
        return self.rol == self.Roles.PROFESOR
