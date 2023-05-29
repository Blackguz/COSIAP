from django.db import models
from usuarios.models import Solicitante


class UsuariosBaneados(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Solicitante, on_delete=models.CASCADE)
    curp = models.CharField(max_length=18)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    class Meta:
        db_table = 'usuarios_baneados'
        verbose_name_plural = 'Usuarios Baneados'
        verbose_name = 'Usuario Baneado'
    def __str__(self):
        return self.usuario