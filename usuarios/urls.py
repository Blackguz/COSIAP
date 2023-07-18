from django.urls import path
from .views import login_view, register_solicitante, logout_view, activate_account, reset_password, reset_confirm

app_name = 'usuarios'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('registro/', register_solicitante, name='registro'),
    path('logout/', logout_view, name='cerrar_sesion'),
    path('reset-passwrd/', reset_password, name='recuperar_password'),
    path('reset/<uidb64>/<token>/', reset_confirm, name='password_reset_confirm'),
    path('activar_cuenta/<uidb64>/<token>/', activate_account, name='activar_cuenta')
]
