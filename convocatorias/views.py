from django.shortcuts import render, redirect, get_object_or_404
from soporte.forms import SolicitudApoyoForm
from .utils import procesar_becas
from .models import Modalidad, Formulario, AtributosFormulario
from convocatorias.forms import AtributoFormularioForm

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
    if request.method == 'POST':
        atributo = "Añadir documento"
        id_formulario = request.POST["id_formulario"]
        atributosFormulario = AtributosFormulario.objects.filter(id_formulario=id_formulario)
        arregloAtributos = []
        return redirect("/solicitud_de_apoyos/6")
    else:
        modalidad = get_object_or_404(Modalidad, pk=id)
        formulario = get_object_or_404(Formulario, pk=id)
        atributosFormulario = AtributosFormulario.objects.filter(id_formulario=formulario.pk)

        return render(request, 'solicitud_apoyo.html', {'modalidad': modalidad, 'formulario':formulario, 'atributos':atributosFormulario})