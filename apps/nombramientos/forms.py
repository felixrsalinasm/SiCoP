from django import forms
from .models import CatTipoNombramiento, Nombramiento, NombramientoProfesor, ProgramaNombramiento

class FormularioTipoNombramiento(forms.ModelForm):
    class Meta:
        model = CatTipoNombramiento
        fields = ['nombramiento', 'origen', 'descripcion']

class FormularioNombramiento(forms.ModelForm):
    class Meta:
        model = Nombramiento
        fields = ['clave', 'fecha_emision', 'fecha_vencimiento', 'tipo', 'observaciones', 'archivo']
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_emision = cleaned_data.get('fecha_emision')
        fecha_vencimiento = cleaned_data.get('fecha_vencimiento')

        if fecha_emision and fecha_vencimiento and fecha_vencimiento <= fecha_emision:
            self.add_error('fecha_vencimiento', 'La fecha de vencimiento debe ser posterior a la de emisión.')
        return cleaned_data

class FormularioNombramientoProfesor(forms.ModelForm):
    class Meta:
        model = NombramientoProfesor
        fields = ['profesor', 'nombramiento']

class FormularioNombramientoPrograma(forms.ModelForm):
    class Meta:
        model = ProgramaNombramiento
        fields = ['programa', 'nombramiento']
