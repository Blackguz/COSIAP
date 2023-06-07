from django.shortcuts import render, redirect, get_object_or_404
from soporte.forms import SolicitudApoyoForm
from .utils import procesar_becas
from .models import Modalidad, Formulario

# Create your views here.

def index(request):
    if request.method == 'POST':
        formulario_solicitud = SolicitudApoyoForm(request.POST)
        if formulario_solicitud.is_valid():
            formulario_solicitud.save()
            return redirect('index')
    else:
        formulario_solicitud = SolicitudApoyoForm()
    return render(request, 'index.html', {'form': formulario_solicitud, **procesar_becas()})

def solicitud_de_apoyos(request, id):
    modalidad = get_object_or_404(Modalidad, pk=id)
    formulario = get_object_or_404(Formulario, pk=modalidad.nombre)
    return render(request, 'solicitud_apoyo.html', {'modalidad': modalidad, 'formulario':formulario})

