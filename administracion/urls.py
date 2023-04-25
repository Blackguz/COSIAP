from django.urls import path
from .views import *

app_name = 'administracion'

urlpatterns = [
    path('panel/', panel_administracion, name='panel'),
    path('usuarios/', lista_usuarios, name='usuarios'),
    path('usuarios/eliminar/<int:id>', eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/editar/<int:id>', editar_usuario, name='editar_usuario'),
    path('usuarios/crear/', crear_usuario, name='crear_usuario'),
    path('administradores/', lista_administradores, name='administradores'),
    path('administradores/crear/', crear_administrador, name='crear_administrador'),
    path('administradores/editar/<int:id>', editar_administrador, name='editar_administrador'),
    path('banear_usuario/<int:id>', banear_usuario, name='banear_usuario'),
    path('desbanear_usuario/<int:id>', desbanear_usuario, name='desbanear_usuario'),
    path('enviar_correo/<int:id>', enviar_correo, name='enviar_correo'),
    path('modalidades/', lista_modalidades, name='modalidades'),
    path('modalidades/crear/', crear_modalidad, name='crear_modalidad'),
]
