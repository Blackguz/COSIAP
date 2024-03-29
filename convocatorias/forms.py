from django import forms
from convocatorias.models import Modalidad, Estatus, Formulario, AtributosFormulario
from django.core.exceptions import ValidationError

class ModalidadForm(forms.ModelForm):
    """
    ModelForm class for creating and updating instances of the Modalidad model.

    This form is a ModelForm that corresponds to the Modalidad model. It includes fields for 'nombre', 'descripcion',
    'requisitos', 'fecha_inicio', 'fecha_fin', 'presupuesto', and 'estatus'. Each field is mapped to the corresponding
    model field, and they are customized using widgets to provide a consistent and user-friendly interface.

    Attributes:
        Meta (class): A nested class that defines metadata options for the form.
        clean() (method): Custom validation method to check if 'fecha_fin' is not earlier than 'fecha_inicio'.
    """
    class Meta:
        model = Modalidad
        fields = [
            'nombre',
            'descripcion',
            'requisitos',
            'fecha_inicio',
            'fecha_fin',
            'presupuesto',
            'estatus',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'requisitos': forms.Textarea(attrs={'class': 'form-control'}),
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
    """
    ModelForm class for creating and updating instances of the Formulario model.

    This form is a ModelForm that corresponds to the Formulario model. It includes fields for 'nombre' and 'id_modalidad'.
    Each field is mapped to the corresponding model field, and they are customized using widgets and labels to provide
    a consistent and user-friendly interface.

    Attributes:
        Meta (class): A nested class that defines metadata options for the form.
    """
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
    """
    ModelForm class for creating and updating instances of the AtributosFormulario model.

    This form is a ModelForm that corresponds to the AtributosFormulario model. It includes fields for 'nombre',
    'tipo_atributo', and 'es_documento'. Each field is mapped to the corresponding model field, and they are customized
    using widgets and labels to provide a consistent and user-friendly interface.

    Attributes:
        Meta (class): A nested class that defines metadata options for the form.
    """
    class Meta:
        model = AtributosFormulario
        fields = ['nombre', 'tipo_atributo', 'es_documento']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_atributo': forms.Select(attrs={'class': 'form-select'}),
            'es_documento': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre': 'Nombre del atributo',
            'tipo_atributo': 'Tipo de atributo',
            'es_documento': 'Es documento',
        }
