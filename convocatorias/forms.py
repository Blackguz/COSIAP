from django import forms
from convocatorias.models import Modalidad, Estatus, Formulario, AtributosFormulario
from django.core.exceptions import ValidationError

class ModalidadForm(forms.ModelForm):
    class Meta:
        model = Modalidad
        fields = [
            'nombre',
            'descripcion',
            'fecha_inicio',
            'fecha_fin',
            'presupuesto',
            'estatus',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'presupuesto': forms.NumberInput(attrs={'class': 'form-control'}),
            'estatus': forms.Select(attrs={'class': 'form-control'}),
        }


    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                raise ValidationError("La fecha de finalización no puede ser anterior a la fecha de inicio.")
            
class FormularioForm(forms.ModelForm):
    class Meta:
        model = Formulario
        fields = ['nombre', 'id_modalidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'id_modalidad': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nombre': 'Nombre del formulario',
            'id_modalidad': 'Modalidad',
        }

class AtributoFormularioForm(forms.ModelForm):
    class Meta:
        model = AtributosFormulario
        fields = ['nombre', 'tipo_atributo', 'es_documento', 'archivo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_atributo': forms.TextInput(attrs={'class': 'form-control'}),
            'es_documento': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'archivo': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre del atributo',
            'tipo_atributo': 'Tipo de atributo',
            'es_documento': 'Es documento',
            'archivo': 'Archivo',
        }

    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if archivo:
            # Validar que el archivo sea un PDF
            content_type = archivo.content_type
            if content_type != 'application/pdf':
                raise ValidationError('El archivo debe ser un PDF.')

            # Validar que el archivo no sea mayor a 3 MB
            max_size_mb = 3
            max_size_bytes = max_size_mb * 1024 * 1024
            if archivo.size > max_size_bytes:
                raise ValidationError(f'El archivo no debe ser mayor a {max_size_mb} MB.')

        return archivo