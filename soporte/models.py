from django.db import models
from usuarios.models import Administrador

# Create your models here.
class SolicitudSoporte(models.Model):
    ESTADOS = [
        ('EN', 'En espera'),
        ('EA', 'En Atencion'),
        ('AT', 'Atendido'),
    ]

    nombre = models.CharField(max_length=200)
    correo = models.EmailField(max_length=200)
    telefono = models.CharField(max_length=10)
    asunto = models.CharField(max_length=200)
    comentarios = models.TextField()
    estado = models.CharField(
        max_length=2,
        choices=ESTADOS,
        default='EN',
    )
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'SolicitudApoyo {self.id}: {self.__dict__}'
