from django.urls import path
from .views import login_view, register_solicitante

app_name = 'usuarios'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('registro/', register_solicitante, name='registro'),
]
