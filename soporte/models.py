from django.db import models

# Create your models here.
class SolicitudApoyo(models.Model):
    estado_solicitud = models.CharField(max_length=255)
    nombre = models.CharField(max_length=50)
    correo = models.CharField(max_length=80)
    telefono = models.DecimalField(max_digits=10, decimal_places=0)
    asunto = models.CharField(max_length=80)
    comentarios = models.CharField(max_length=500)

    def __str__(self):
        return f'SolicitudApoyo {self.id}: {self.__dict__}'
