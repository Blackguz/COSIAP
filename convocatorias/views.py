from django.shortcuts import render, redirect
from soporte.forms import SolicitudApoyoForm
from .models import Modalidad

# Create your views here.

def obtener_becas(limite: int) -> list[Modalidad]:
    return Modalidad.objects.all()[:limite]

def index(request):
    if request.method == 'POST':
        formulario_solicitud = SolicitudApoyoForm(request.POST)
        if formulario_solicitud.is_valid():
            formulario_solicitud.save()
            return redirect('index')
    else:
        formulario_solicitud = SolicitudApoyoForm()
    return render(request, 'index.html', {'form': formulario_solicitud, "becas": obtener_becas(3)})

def solicitud_de_apoyos(request):
    return render(request, 'solicitud_apoyo.html')
