from django import forms
from .models import Laboratorio, Programa, Coordinador


class FormularioLaboratorio(forms.ModelForm):
    class Meta:
        model = Laboratorio
        fields = ['nombre', 'siglas', 'jefe']


class FormularioPrograma(forms.ModelForm):
    class Meta:
        model = Programa
        fields = ['nombre', 'siglas', 'nivel', 'duracion_maxima_meses', 'url_doc_base', 'fecha_creacion', 'activo']
        widgets = {
            'fecha_creacion': forms.DateInput(attrs={'type': 'date'}),
        }


class FormularioCoordinador(forms.ModelForm):
    class Meta:
        model = Coordinador
        fields = ['profesor', 'programa', 'fecha_inicio']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
        }
