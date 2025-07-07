from django import forms
from .models import Taller

class ProponerTallerForm(forms.ModelForm):
    class Meta:
        model = Taller
        fields = ['titulo', 'fecha', 'duracion_horas', 'lugar', 'categoria']
        labels = {
            'titulo': 'Titulo del taller',
            'fecha': 'Fecha',
            'duracion_horas': 'Duración (horas)',
            'lugar': 'Lugar',
            'categoria': 'Categoria'
        }
        widgets = {
            'titulo': forms.TextInput(attrs= {'class':'form-control'}),
            'fecha': forms.DateInput(attrs = {'type': 'date', 'class':'form-control'}),
            'duracion_horas': forms.NumberInput(attrs= {'class':'form-control'}),
            'lugar': forms.Select(attrs= {'class':'form-control'}),
            'categoria': forms.Select(attrs= {'class':'form-control'})
        }