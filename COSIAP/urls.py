"""COSIAP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from convocatorias.views import index, solicitud_de_apoyos, solicitudes_realizadas, lista_apoyos

app_name = 'COSIAP'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('soporte/', include('soporte.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('administracion/', include('administracion.urls')),
    path('', index, name='index'),
    path('solicitud_de_apoyos/<int:idModalidad>', solicitud_de_apoyos, name="solicitud_de_apoyos"),
    path('solicitudes_realizadas/', solicitudes_realizadas, name="solicitudes_realizadas"),
    path('lista_apoyos/', lista_apoyos, name="lista_apoyos")
]
