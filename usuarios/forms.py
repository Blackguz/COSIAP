from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Solicitante, Administrador

# Validamos correo electronico que no este en uso
def validate_email_unique(value):
    if Solicitante.objects.filter(email=value).exists() or Administrador.objects.filter(email=value).exists():
        raise ValidationError("El correo electrónico ya está en uso.")
class SolicitanteCreationForm(UserCreationForm):
    email = forms.EmailField(validators=[validate_email_unique])
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
            'curp',
            'ultimo_grado_estudios',
            'institucion',
            'domicilio_calle',
            'domicilio_numero_exterior',
            'domicilio_numero_interior',
            'domicilio_codigo_postal',
        )
        def clean_genero(self):
            genero = self.cleaned_data['genero']
            if genero not in ['M', 'F']:
                raise forms.ValidationError('El género debe ser Masculino o Femenino')
            return genero
        
class AdministradorForm(forms.ModelForm):

    email = forms.EmailField(validators=[validate_email_unique])
    class Meta:
        model = Administrador
        fields = [
            'username',
            'first_name',
            'email',
            'password1',
            'password2',
            'apellido_paterno',
            'apellido_materno',
            'telefono_celular',
            'nivel_acceso',
        ]

    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput,
    )

    password2 = forms.CharField(
        label="Confirma Contraseña",
        strip=False,
        widget=forms.PasswordInput,
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    