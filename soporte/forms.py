from django.forms import ModelForm, EmailInput, TextInput, NumberInput, Textarea
from soporte.models import SolicitudSoporte

input_classes = {'class': 'regular-input'}

class SolicitudSoporteForm(ModelForm):
    class Meta:
        model = SolicitudSoporte
        exclude = ['estado_solicitud']
        widgets = {
            'nombre': TextInput(attrs={'placeholder': 'Tu nombre*', **input_classes}),
            'correo': EmailInput(attrs={'type': 'email', 'placeholder': 'Tu E-mail*', **input_classes}),
            'telefono': NumberInput(attrs={'type': 'number', 'placeholder': 'Telefono*', **input_classes}),
            'asunto': TextInput(attrs={'placeholder': 'Asunto*', **input_classes}),
            'comentarios': Textarea(attrs={'placeholder': 'Escribe tu comentario aquí*', **input_classes})
        }


