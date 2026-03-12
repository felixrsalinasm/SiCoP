from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import DirectorTesis, ComiteTutorial, JuradoExamen
from apps.personas.models import Profesor

class FormularioDirectorTesis(forms.ModelForm):
    class Meta:
        model = DirectorTesis
        fields = ['estudiante', 'profesor', 'es_codirector', 'fecha_asignacion']
        widgets = {
            'fecha_asignacion': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profesor'].queryset = Profesor.objects.filter(activo=True)

class FormularioComiteTutorial(forms.ModelForm):
    class Meta:
        model = ComiteTutorial
        fields = ['estudiante', 'profesor', 'fecha_asignacion']
        widgets = {
            'fecha_asignacion': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profesor'].queryset = Profesor.objects.filter(activo=True)

class FormularioJuradoExamen(forms.ModelForm):
    class Meta:
        model = JuradoExamen
        fields = ['estudiante', 'profesor', 'tipo_examen', 'rol', 'fecha_examen']
        widgets = {
            'fecha_examen': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Include all professors (internal and external)
        self.fields['profesor'].queryset = Profesor.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        estudiante = cleaned_data.get('estudiante')
        profesor = cleaned_data.get('profesor')
        tipo_examen = cleaned_data.get('tipo_examen')
        rol = cleaned_data.get('rol')

        if not (estudiante and profesor and tipo_examen and rol):
            return cleaned_data

        qs = JuradoExamen.objects.filter(estudiante=estudiante, tipo_examen=tipo_examen)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        # 1. Máximo 5 titulares (PRESIDENTE + SECRETARIO + VOCAL)
        if rol in [JuradoExamen.RolJurado.PRESIDENTE, JuradoExamen.RolJurado.SECRETARIO, JuradoExamen.RolJurado.VOCAL]:
            titulares = qs.filter(rol__in=[JuradoExamen.RolJurado.PRESIDENTE, JuradoExamen.RolJurado.SECRETARIO, JuradoExamen.RolJurado.VOCAL]).count()
            if titulares >= 5:
                raise ValidationError('Ya existen 5 titulares registrados para este examen.')

        # 2. Máximo 1 SUPLENTE
        if rol == JuradoExamen.RolJurado.SUPLENTE:
            suplentes = qs.filter(rol=JuradoExamen.RolJurado.SUPLENTE).count()
            if suplentes >= 1:
                raise ValidationError('Solo puede haber 1 suplente registrado para este examen.')

        # 3. Máximo 2 externos
        if profesor.es_externo:
            externos = qs.filter(profesor__es_externo=True).count()
            if externos >= 2:
                raise ValidationError('No puede haber más de 2 profesores externos en el jurado.')

        # 4. El director activo del estudiante debe estar en el jurado. 
        # Actually this validation might be tricky to enforce strictly element-by-element since they are added one by one.
        # But if the requirement implies that the director must be part of it, maybe we don't block saving if the current one isn't the director, but we could check if it is the LAST spot. We'll leave the strict block out if the user is just building the committee, since they add them one by one. But wait, the instruction says:
        # "El director de tesis debe formar parte del jurado" -> we might not block adding someone else, but it's a rule. We will just ensure that if they are adding someone, it's fine. If we must block, when is it blocked?
        # Actually, let's just make sure we don't block adding other members, because they have to add 5 members. If they add vocal #1 and it's not the director, we can't block it.
        # So we won't raise an error for #4 on every single addition, unless we enforce it at the end, which we can't easily do in a single-instance form. Wait, we could add a warning or form clean validation if it's the last titanium. I will skip hard blocking for #4 here to avoid chicken-and-egg, or I'll just validate that if they reach 6 members, the director must be there.
        # Wait, if they are adding the 6th member, and the director is not in the set, we can block.
        total_miembros = qs.count()
        if total_miembros == 5:
            # Check if director is already in qs or is the current one
            directores = DirectorTesis.objects.filter(estudiante=estudiante, activo=True).values_list('profesor_id', flat=True)
            jurado_profesores = list(qs.values_list('profesor_id', flat=True)) + [profesor.id]
            if directores and not any(d in jurado_profesores for d in directores):
                raise ValidationError('El director de tesis activo debe formar parte del jurado. No se puede completar el jurado sin él.')

        return cleaned_data
