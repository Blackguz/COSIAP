from django.db import models
from django.contrib.auth.models import User

class Solicitante(User):
    
    GENERO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )

    apellido_materno = models.CharField(max_length=30)
    apellido_paterno = models.CharField(max_length=30)
    telefono_particular = models.CharField(max_length=20)
    telefono_celular = models.CharField(max_length=20)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    ultimo_grado_estudios = models.CharField(max_length=20)
    institucion = models.CharField(max_length=100)
    domicilio_calle = models.CharField(max_length=100)
    domicilio_numero_exterior = models.CharField(max_length=10)
    domicilio_numero_interior = models.CharField(max_length=10, blank=True, null=True)
    domicilio_codigo_postal = models.CharField(max_length=5)

    class Meta:
        verbose_name_plural = "Solicitantes"

class Administrador(User):
    NIVEL_ACCESO = (
        ('N1', 'Nivel 1'),
        ('N2', 'Nivel 2'),
        ('N3', 'Nivel 3'),
    )
    apellido_materno = models.CharField(max_length=30)
    apellido_paterno = models.CharField(max_length=30)
    telefono_celular = models.CharField(max_length=20)
    nivel_acceso = models.CharField(max_length=2, choices=NIVEL_ACCESO)

    class Meta:
        verbose_name_plural = "Administradores"
