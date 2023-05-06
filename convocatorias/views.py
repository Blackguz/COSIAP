from django.shortcuts import render, redirect
from soporte.forms import SolicitudApoyoForm
from .models import Modalidad

# Create your views here.

def obtener_becas(limite: int) -> list[Modalidad]:
    return Modalidad.objects.all()[:limite]

def obtener_disposicion(tamano_becas: int) -> str:
    return "" if tamano_becas >= 3 else "gdisp2" if tamano_becas == 2 else "gdisp1"
def procesar_becas() -> dict:
    diccionario_becas = {
        "becas": {
            "becas": (becas := obtener_becas(3)),
            "disposicion": obtener_disposicion(len(becas))
        }
    }
    return diccionario_becas
def index(request):
    if request.method == 'POST':
        formulario_solicitud = SolicitudApoyoForm(request.POST)
        if formulario_solicitud.is_valid():
            formulario_solicitud.save()
            return redirect('index')
    else:
        formulario_solicitud = SolicitudApoyoForm()
    return render(request, 'index.html', {'form': formulario_solicitud, **procesar_becas()})

def solicitud_de_apoyos(request):
    return render(request, 'solicitud_apoyo.html')
