from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Solicitante

class SolicitanteCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Solicitante
        fields = UserCreationForm.Meta.fields + (
            'first_name',
            'email',
            'apellido_materno',
            'apellido_paterno',
            'telefono_particular',
            'telefono_celular',
            'genero',
            'ultimo_grado_estudios',
            'institucion',
            'domicilio_calle',
            'domicilio_numero_exterior',
            'domicilio_numero_interior',
            'domicilio_codigo_postal',
        )