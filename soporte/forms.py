from django.forms import ModelForm, EmailInput, TextInput, NumberInput, Textarea
from soporte.models import SolicitudSoporte

input_classes = {'class': 'input_container'}

class SolicitudSoporteForm(ModelForm):
    class Meta:
        model = SolicitudSoporte
        exclude = ['estado_solicitud']
        widgets = {
            'nombre': TextInput(attrs={'placeholder': 'Tu nombre*', 'title': 'Nombre*', **input_classes}),
            'correo': EmailInput(attrs={'type': 'email', 'placeholder': 'Tu E-mail*', 'title': 'E-mail*', **input_classes}),
            'telefono': NumberInput(attrs={'type': 'number', 'placeholder': 'Telefono*', 'title': 'Teléfono*',**input_classes}),
            'asunto': TextInput(attrs={'placeholder': 'Asunto*','title': 'Asunto*', **input_classes}),
            'comentarios': Textarea(attrs={'placeholder': 'Escribe tu comentario aquí*','title': 'Escribe tu comentario aquí*', **input_classes})
        }


