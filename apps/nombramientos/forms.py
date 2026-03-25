from django import forms
from .models import CatTipoNombramiento, Nombramiento, NombramientoProfesor, ProgramaNombramiento


class FormularioTipoNombramiento(forms.ModelForm):
    class Meta:
        model = CatTipoNombramiento
        fields = ['nombramiento', 'origen', 'descripcion']


class FormularioNombramiento(forms.ModelForm):
    class Meta:
        model = Nombramiento
        fields = ['profesor', 'tipo', 'clave', 'fecha_inicio', 'fecha_fin',
                  'fecha_emision', 'fecha_vencimiento', 'observaciones', 'archivo']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'fecha_emision': forms.DateInput(attrs={'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }


class FormularioNombramientoProfesor(forms.ModelForm):
    class Meta:
        model = NombramientoProfesor
        fields = ['profesor', 'nombramiento']


class FormularioNombramientoPrograma(forms.ModelForm):
    class Meta:
        model = ProgramaNombramiento
        fields = ['programa', 'nombramiento']
