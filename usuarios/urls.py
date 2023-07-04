from django.urls import path
from .views import login_view, register_solicitante, logout_view, activate_account

app_name = 'usuarios'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('registro/', register_solicitante, name='registro'),
    path('logout/', logout_view, name='cerrar_sesion'),
    path('activar_cuenta/<uidb64>/<token>/', activate_account, name='activar_cuenta')
]
