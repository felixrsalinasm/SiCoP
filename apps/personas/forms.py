from django import forms
from django.core.validators import RegexValidator
from .models import Persona, Profesor, Estudiante

class FormularioPersona(forms.ModelForm):
    rfc = forms.CharField(
        max_length=13,
        min_length=13,
        required=False,
        validators=[RegexValidator(r'^[A-Z0-9]{13}$', 'RFC debe tener 13 caracteres alfanuméricos.')]
    )
    curp = forms.CharField(
        max_length=18,
        min_length=18,
        required=False,
        validators=[RegexValidator(r'^[A-Z0-9]{18}$', 'CURP debe tener 18 caracteres alfanuméricos.')]
    )
    cvu = forms.CharField(
        max_length=10,
        required=False,
        validators=[RegexValidator(r'^\d{1,10}$', 'CVU debe contener solo números (máximo 10).')]
    )

    class Meta:
        model = Persona
        fields = [
            'nombres', 'paterno', 'materno', 'email', 'telefono',
            'genero', 'fecha_nacimiento', 'rfc', 'curp', 'cvu', 'foto'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

class FormularioProfesor(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = [
            'grado_academico', 'laboratorio', 'fecha_ingreso_ipn',
            'fecha_ingreso_cic', 'es_externo', 'activo'
        ]
        widgets = {
            'fecha_ingreso_ipn': forms.DateInput(attrs={'type': 'date'}),
            'fecha_ingreso_cic': forms.DateInput(attrs={'type': 'date'}),
        }

class FormularioEstudiante(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = [
            'matricula', 'programa', 'generacion', 'modalidad',
            'estado', 'fecha_ingreso', 'fecha_egreso'
        ]
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
            'fecha_egreso': forms.DateInput(attrs={'type': 'date'}),
        }
