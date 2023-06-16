from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
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
    path('modalidades/eliminar/<int:id>', eliminar_modalidad, name='eliminar_modalidad'),
    path('modalidades/editar/<int:id>', editar_modalidad, name='editar_modalidad'),
    path('crear_formulario/', crear_formulario, name='crear_formulario'),
    path('lista_formularios/', lista_formularios, name='lista_formularios'),
    path('actualizar_formulario/', actualizar_formulario, name='actualizar_formulario'),
    path('eliminar_formulario/<int:id>', eliminar_formulario, name='eliminar_formulario'),
    path('papelera/modalidades', papelera_modalidades, name='modalidades_eliminadas'),
    path('papelera/restaurar/<int:id>/', restaurar_modalidad, name='restaurar_modalidad'),
    path('papelera/usuarios/', papelera_usuarios, name='papelera_usuarios'),
    path('papelera/restaurar_usuario/<int:id>/', restaurar_usuario, name='restaurar_usuario'),
    path('papelera/baneados/', lista_baneados, name='baneados'),
    path('solicitudes/nuevas/', solicitudes_apoyos_nuevas, name='solicitudes_apoyos_nuevas'),
    path('descarga/documento/<int:pk>', download_documento, name='download_documento'),
    path('solicitud/cambiar_estado/<int:estado>/<int:solicitud>/', cambiar_estado, name='cambiar_estado'),
    path('solicitud/actualizar_solicitud/<int:id>/', actualizar_solicitud, name='actualizar_solicitud'),
    path('solicitud/en_proceso/', solicitudes_apoyos_proceso, name='solicitudes_en_proceso'),
    path('solicitud/aprovadas/', solicitudes_aprovadas, name='solicitudes_aprovadas'),
    path('solicitud/finalizadas/', solicitudes_finalizadas, name='solicitudes_finalizadas')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
