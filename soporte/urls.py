from django.urls import path
from .views import SolicitudesEnEsperaView, SolicitudesEnAtencionView, SolicitudesAtendidasView, cambiar_estado_solicitud, CrearSolicitudView


app_name = 'soporte'

urlpatterns = [
    path('espera/', SolicitudesEnEsperaView.as_view(), name='solicitudes_espera'),
    path('atencion/', SolicitudesEnAtencionView.as_view(), name='solicitudes_atencion'),
    path('atendidas/', SolicitudesAtendidasView.as_view(), name='solicitudes_atendidas'),
    path('cambiar_estado/<int:id_solicitud>/<str:nuevo_estado>/', cambiar_estado_solicitud, name='cambiar_estado'),
    path('crear_solicitud/', CrearSolicitudView.as_view(), name='crear_solicitud'),
]