import os
from django.db import models
from usuarios.models import Solicitante
from django.utils import timezone

class Estatus(models.Model):
    id_estatus = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Modalidad(models.Model):
    id_modalidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
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
    estado = models.CharField(max_length=255)

    def __str__(self):
        return f'Formulario {self.id_formulario} - {self.id_modalidad.nombre}'

class AtributosFormulario(models.Model):
    id_atributos_formularios = models.AutoField(primary_key=True)
    id_formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    tipo_atributo = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.nombre} - {self.tipo_atributo}'

