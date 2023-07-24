from django.db import models
from usuarios.models import Solicitante


class UsuariosBaneados(models.Model):
    """
    Un modelo que representa a un usuario que ha sido baneado.

    Atributos:
    id (AutoField): El ID del usuario baneado. Este campo es la clave primaria.
    usuario (ForeignKey): La referencia al usuario que ha sido baneado. Se relaciona con el modelo Solicitante.
    curp (CharField): El CURP del usuario baneado.
    fecha (DateField): La fecha en que el usuario fue baneado. Se añade automáticamente cuando se crea el registro.
    hora (TimeField): La hora en que el usuario fue baneado. Se añade automáticamente cuando se crea el registro.

    Meta:
    db_table: El nombre de la tabla en la base de datos es 'usuarios_baneados'.
    verbose_name_plural: El nombre plural para mostrar en el administrador de Django es 'Usuarios Baneados'.
    verbose_name: El nombre singular para mostrar en el administrador de Django es 'Usuario Baneado'.
    """
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Solicitante, on_delete=models.CASCADE, default=None)
    curp = models.CharField(max_length=18)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    class Meta:
        db_table = 'usuarios_baneados'
        verbose_name_plural = 'Usuarios Baneados'
        verbose_name = 'Usuario Baneado'
    def __str__(self):
        return str(self.usuario)