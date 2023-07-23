from django import forms
from .models import SolicitudSoporte

class SolicitudSoporteForm(forms.ModelForm):
    class Meta:
        model = SolicitudSoporte
        fields = ['nombre', 'correo', 'telefono', 'asunto', 'comentarios']