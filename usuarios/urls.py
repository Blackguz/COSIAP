from django.urls import path
from .views import login_view, register_solicitante

urlpatterns = [
    path('login/', login_view, name='login'),
    path('registro/', register_solicitante, name='registro'),
]
