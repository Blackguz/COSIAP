from django.shortcuts import render, redirect, get_object_or_404
from soporte.forms import SolicitudSoporteForm
from usuarios.models import Solicitante
from .utils import procesar_becas, numero_becas
from .models import Modalidad, Formulario, AtributosFormulario, Solicitud, Estatus, DocumentoSolicitud
from convocatorias.forms import AtributoFormularioForm
from datetime import datetime
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.http import FileResponse
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
    return render(request, 'index.html', {'form': formulario_solicitud, "modalidades":procesar_becas()})

def solicitud_de_apoyos(request, idModalidad):
    if request.method == 'POST':
        id_formulario = request.POST["id_formulario"]
        atributosFormulario = AtributosFormulario.objects.filter(id_formulario=id_formulario)
        solicitante = Solicitante.objects.get(id=request.user.pk)
        estatus = get_object_or_404(Estatus, pk=1)
        monto_solicitud = request.POST["monto_solicitado"]
        modalidad = get_object_or_404(Modalidad, pk=idModalidad)
        solicitud = Solicitud.objects.create(monto_solicitado=monto_solicitud, monto_aprobado=0 ,fecha_solicitud=datetime.now(), id_estatus=estatus, id_modalidad=modalidad, id_solicitante=solicitante, observaciones=request.POST['notas_adicionales'])
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
        modalidad = Modalidad.objects.get(pk=idModalidad)
        try:
            formulario = Formulario.objects.get(id_modalidad=modalidad)
            atributosFormulario = AtributosFormulario.objects.filter(id_formulario=formulario)
        except Formulario.DoesNotExist:
            formulario = []
            atributosFormulario = []

        return render(request, 'solicitud_apoyo.html', {'modalidad': modalidad, 'formulario':formulario, 'atributos':atributosFormulario})


def solicitudes_realizadas(request):
    solicitudes_list = Solicitud.objects.all()
    paginator = Paginator(solicitudes_list, 6)  # Mostrar 6 solicitudes por página.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    pag_actual = int(page_number) if page_number else 1
    page_range = paginator.get_elided_page_range(number=pag_actual, on_each_side=2, on_ends=1)

    return render(request, 'solicitudes_realizadas.html', {'page_obj': page_obj, 'page_range':page_range})


def detalle_solicitud(request, id_solicitud):
    solicitud = Solicitud.objects.get(pk=id_solicitud)

    data = {
        'nombre': solicitud.id_modalidad.nombre,
        'descripcion': solicitud.id_modalidad.descripcion,
        'monto': str(solicitud.monto_solicitado),  # Convertimos Decimal a string para la serialización
    }

    return JsonResponse(data)

"""
def lista_apoyos(request):
    if request.method == 'POST':
        formulario_solicitud = SolicitudSoporteForm(request.POST)
        if formulario_solicitud.is_valid():
            formulario_solicitud.save()
            return redirect('lista_apoyos')
    else:
        formulario_solicitud = SolicitudSoporteForm()
    return render(request, 'lista_apoyos.html', {'form': formulario_solicitud, **obtener_todas()})
"""


def lista_apoyos(request):
    contact_list = numero_becas()
    paginator = Paginator(contact_list, 6)

    page_number = request.GET.get("page",1)
    page_obj = paginator.get_page(page_number)

    page_numero = request.GET.get('page')
    pag_actual = int(page_numero) if page_numero else 1

    page_range = paginator.get_elided_page_range(number=pag_actual,on_each_side=2,on_ends=1)

    lista_modalidaes=list(page_obj)

    return render(request, "lista_apoyos.html", {"page_obj": page_obj, "modalidades":procesar_becas(lista_modalidaes),"page_range":page_range})


def download_pdf(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'reglas_operacion', 'reglas_operacion2023.pdf')
    file = open(file_path, 'rb')
    response = FileResponse(file, as_attachment=True, filename='reglas_operacion2023.pdf')
    return response
