from django.db import models
from usuarios.models import Solicitante
from django.utils import timezone
from .utils import user_directory_path
class Estatus(models.Model):
    id_estatus = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Modalidad(models.Model):
    id_modalidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    requisitos = models.TextField(null=True, blank=True, default='sin requisitos')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2)
    estatus = models.ForeignKey('convocatorias.Estatus', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Solicitud(models.Model):
    monto_solicitado = models.DecimalField(max_digits=10, decimal_places=2)
    documentos = models.FileField(blank=True, null=True)
    estado = models.CharField(max_length=255)
    monto_aprobado = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_solicitud = models.DateField()
    id_estatus = models.ForeignKey(Estatus, on_delete=models.CASCADE)
    id_modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE)
    id_solicitante = models.ForeignKey(Solicitante, on_delete=models.CASCADE) # Modelo personalizado 'Solicitante'
    observaciones = models.TextField()
    id_solicitud = models.AutoField(primary_key=True)

    def __str__(self):
        return f'Solicitud {self.id_solicitud} - {self.id_solicitante.username}'

class Formulario(models.Model):
    id_formulario = models.AutoField(primary_key=True)
    id_modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255, default='sin nombre')
    estatus = models.ForeignKey('convocatorias.Estatus', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Formulario {self.id_formulario} - {self.id_modalidad.nombre}'

class AtributosFormulario(models.Model):
    TIPO_OPCIONES = [
        ('Texto', 'Texto'),
        ('Numero', 'Numero'),
        ('Fecha', 'Fecha'),
        ('Documento', 'Documento'),
        ('Telefono', 'Telefono'),
    ]
    id_atributos_formularios = models.AutoField(primary_key=True)
    id_formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=85)
    tipo_atributo = models.CharField(max_length=15, choices=TIPO_OPCIONES)
    es_documento = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nombre} - {self.tipo_atributo}'

