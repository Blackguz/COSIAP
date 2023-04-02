from django.urls import path
from .views import login, register_solicitante

urlpatterns = [
    path('login/', login, name='login'),
    path('registro/', register_solicitante, name='registro'),
]
