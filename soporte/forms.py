from django.forms import ModelForm, EmailInput, TextInput, NumberInput, Textarea
from convocatorias.models import SolicitudApoyo

input_classes = {'class': 'regular-input'}

class SolicitudApoyoForm(ModelForm):
    class Meta:
        model = SolicitudApoyo
        exclude = ['estado_solicitud']
        widgets = {
            'nombre': TextInput(attrs={'placeholder': 'Tu nombre*', **input_classes}),
            'correo': EmailInput(attrs={'type': 'email', 'placeholder': 'Tu E-mail*', **input_classes}),
            'telefono': NumberInput(attrs={'type': 'number', 'placeholder': 'Telefono*', **input_classes}),
            'asunto': TextInput(attrs={'placeholder': 'Asunto*', **input_classes}),
            'comentarios': Textarea(attrs={'placeholder': 'Escribe tu comentario aquí*', **input_classes})
        }
