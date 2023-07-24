from django.db import models
from usuarios.models import Administrador

# Create your models here.
class SolicitudSoporte(models.Model):
    """
    Model class for representing a support request (Solicitud de Apoyo).

    This model class represents a support request (Solicitud de Apoyo) with the following fields:
    - nombre: The name of the requester (CharField).
    - correo: The email of the requester (EmailField).
    - telefono: The phone number of the requester (CharField).
    - asunto: The subject of the support request (CharField).
    - comentarios: Additional comments or details of the support request (TextField).
    - estado: The current state of the support request (choices field with options 'EN', 'EA', 'AT').
    - administrador: The related Administrador object who is handling the support request (ForeignKey).

    Attributes:
        ESTADOS (list): A list of tuples representing the choices for the 'estado' field.
        nombre (CharField): The name of the requester.
        correo (EmailField): The email of the requester.
        telefono (CharField): The phone number of the requester.
        asunto (CharField): The subject of the support request.
        comentarios (TextField): Additional comments or details of the support request.
        estado (CharField): The current state of the support request with choices 'EN' (En espera), 'EA' (En Atencion),
                            or 'AT' (Atendido).
        administrador (ForeignKey): The related Administrador object who is handling the support request.

    Methods:
        __str__(): Return a string representation of the SolicitudSoporte object.

    """
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
