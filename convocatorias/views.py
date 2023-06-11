from django.shortcuts import render, redirect, get_object_or_404
from soporte.forms import SolicitudSoporteForm
from usuarios.models import Solicitante
from .utils import procesar_becas
from .models import Modalidad, Formulario, AtributosFormulario, Solicitud, Estatus, DocumentoSolicitud
from convocatorias.forms import AtributoFormularioForm
from datetime import datetime
from django.contrib import messages
import os
from django.core.files.base import ContentFile
from django.conf import settings

# Create your views here.

def index(request):
    if request.method == 'POST':
        formulario_solicitud = SolicitudSoporteForm(request.POST)
        if formulario_solicitud.is_valid():
            formulario_solicitud.save()
            return redirect('index')
    else:
        formulario_solicitud = SolicitudSoporteForm()
    return render(request, 'index.html', {'form': formulario_solicitud, **procesar_becas()})

def solicitud_de_apoyos(request, idModalidad):
    if request.method == 'POST':
        id_formulario = request.POST["id_formulario"]
        atributosFormulario = AtributosFormulario.objects.filter(id_formulario=id_formulario)
        solicitante = Solicitante.objects.get(id=request.user.pk)
        estatus = get_object_or_404(Estatus, pk=1)
        modalidad = get_object_or_404(Modalidad, pk=idModalidad)
        solicitud = Solicitud.objects.create(monto_solicitado=0, monto_aprobado=0 ,fecha_solicitud=datetime.now(), id_estatus=estatus, id_modalidad=modalidad, id_solicitante=solicitante, observaciones=request.POST['notas_adicionales'])
        non_document_data = {}
        for atributoFormulario in atributosFormulario:
            if atributoFormulario.es_documento:
                valor = request.FILES.get(atributoFormulario.nombre, None)
                if request.FILES[atributoFormulario.nombre].content_type == "application/pdf" and request.FILES[atributoFormulario.nombre].size <= (1024*2*1024):
                    request.FILES[atributoFormulario.nombre].name = atributoFormulario.nombre+".pdf"
                    DocumentoSolicitud.objects.create(solicitud=solicitud, documento=request.FILES[atributoFormulario.nombre]).save()
                else:
                    messages.error(request, "Error al guardar los datos, asegurese de que todos los archivos sean PDF")
                    return redirect(f'/solicitud_de_apoyos/{idModalidad}')
            else: 
                valor = request.POST.get(atributoFormulario.nombre, None)
                non_document_data[atributoFormulario.nombre] = valor

        dataSolicitud_content = '\n'.join(f'{k}:{v}' for k, v in non_document_data.items())
        dataSolicitud_path = 'dataSolicitud.txt'
        DocumentoSolicitud.objects.create(
            solicitud=solicitud,
            documento=ContentFile(dataSolicitud_content.encode(), name=dataSolicitud_path)
        )
        messages.success(request, "Solicitud enviada con éxito")
        return redirect('solicitudes_realizadas')
    else:
        modalidad = get_object_or_404(Modalidad, pk=idModalidad)
        formulario = get_object_or_404(Formulario, pk=idModalidad)
        atributosFormulario = AtributosFormulario.objects.filter(id_formulario=formulario.pk)
        return render(request, 'solicitud_apoyo.html', {'modalidad': modalidad, 'formulario':formulario, 'atributos':atributosFormulario})



def solicitudes_realizadas(request):
    return render(request, 'solicitudes_realizadas.html')




def lista_apoyos(request):
    if request.method == 'POST':
        formulario_solicitud = SolicitudSoporteForm(request.POST)
        if formulario_solicitud.is_valid():
            formulario_solicitud.save()
            return redirect('lista_apoyos')
    else:
        formulario_solicitud = SolicitudSoporteForm()
    return render(request, 'lista_apoyos.html', {'form': formulario_solicitud, **procesar_becas()})