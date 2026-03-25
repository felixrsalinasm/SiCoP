from django import forms
from django.core.exceptions import ValidationError
from .models import Tesis, DirectorTesis, ComiteTutorial, JuradoExamen
from apps.personas.models import Profesor


class FormularioTesis(forms.ModelForm):
    class Meta:
        model = Tesis
        fields = ['titulo', 'resumen', 'estado', 'fecha_registro', 'alumno', 'programa']
        widgets = {
            'fecha_registro': forms.DateInput(attrs={'type': 'date'}),
            'resumen': forms.Textarea(attrs={'rows': 4}),
        }


class FormularioDirectorTesis(forms.ModelForm):
    class Meta:
        model = DirectorTesis
        fields = ['tesis', 'profesor', 'tipo_direccion', 'fecha_asignacion']
        widgets = {
            'fecha_asignacion': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profesor'].queryset = Profesor.objects.filter(activo=True)

    def clean(self):
        cleaned_data = super().clean()
        tesis = cleaned_data.get('tesis')
        profesor = cleaned_data.get('profesor')
        if tesis and profesor:
            qs = DirectorTesis.objects.filter(tesis=tesis, activo=True)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.count() >= 2:
                raise ValidationError('Una tesis no puede tener mas de 2 directores activos.')
        return cleaned_data


class FormularioComiteTutorial(forms.ModelForm):
    class Meta:
        model = ComiteTutorial
        fields = ['tesis', 'profesor', 'rol', 'fecha_asignacion']
        widgets = {
            'fecha_asignacion': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profesor'].queryset = Profesor.objects.filter(activo=True)

    def clean(self):
        cleaned_data = super().clean()
        tesis = cleaned_data.get('tesis')
        if tesis:
            programa = tesis.programa
            if programa.nivel not in ['MAESTRIA', 'DOCTORADO', 'DOCTORADO_DIRECTO']:
                raise ValidationError(
                    'El comite tutorial solo aplica a Maestria, Doctorado o Doctorado Directo.'
                )
        return cleaned_data


class FormularioJuradoExamen(forms.ModelForm):
    class Meta:
        model = JuradoExamen
        fields = ['estudiante', 'profesor', 'tipo_examen', 'rol', 'fecha_examen']
        widgets = {
            'fecha_examen': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profesor'].queryset = Profesor.objects.all()
