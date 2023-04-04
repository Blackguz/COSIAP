from django.urls import path
from .views import panel_administracion

urlpatterns = [
    path('panel/', panel_administracion, name='panel'),
]
