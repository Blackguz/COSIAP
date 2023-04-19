from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from convocatorias.models import Solicitud
from usuarios.models import Solicitante
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from usuarios.forms import SolicitanteCreationForm
from .utils import get_solicitudes_por_nivel, get_generos_solicitantes
import json

# Create your views here.

def panel_administracion(request):
    # Obtenemos el número de solicitudes por nivel de estudios
    estudios_nivel = get_solicitudes_por_nivel()

    # Agregar conteo de género por solicitud
    generos = get_generos_solicitantes()
    
    # Contamos todas las solicitudes
    solicitudes_autorizado = Solicitud.objects.filter(estado='Autorizado').count()
    solicitudes_en_proceso = Solicitud.objects.filter(estado='Documentación completa').count() + Solicitud.objects.filter(estado='Pendiente').count() + Solicitud.objects.filter(estado='En proceso de análisis').count() + Solicitud.objects.filter(estado='Aceptado').count()
    
    # Obtenemos el numero de solicitudes de soporte tecnico pendientes
    #solicitudes_soporte_tecnico = SolicitudSoporte.objects.filter(estado='Pendiente').count()



    context = {
        "niveles_estudios": estudios_nivel[0],
        "solicitudes_por_nivel": estudios_nivel[1],
        "generos": [generos['Masculino'], generos['Femenino']],
        "solicitudes_autorizado": solicitudes_autorizado,
        "solicitudes_en_proceso": solicitudes_en_proceso
    }

    return render(request, "panel.html", context)

def lista_usuarios(request):
    usuarios = Solicitante.objects.all()
    context = {
        "usuarios": usuarios
    }
    return render(request, "lista_usuarios.html", context)

def eliminar_usuario(request, id):
    pass

@login_required
@staff_member_required
def editar_usuario(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        usuario = get_object_or_404(Solicitante, id=id)

        usuario.first_name = data.get("nombre")
        usuario.apellido_materno = data.get("apellido_materno")
        usuario.apellido_paterno = data.get("apellido_paterno")
        usuario.telefono_particular = data.get("telefono_particular")
        usuario.telefono_celular = data.get("telefono_celular")
        usuario.genero = data.get("genero")
        usuario.ultimo_grado_estudios = data.get("ultimo_grado_estudios")
        usuario.institucion = data.get("institucion")
        usuario.domicilio_calle = data.get("domicilio_calle")
        usuario.domicilio_numero_exterior = data.get("domicilio_numero_exterior")
        usuario.domicilio_numero_interior = data.get("domicilio_numero_interior")
        usuario.domicilio_codigo_postal = data.get("domicilio_codigo_postal")

        try:
            usuario.save()
            return JsonResponse({"status": "success"}, status=200)
        except:
            return JsonResponse({"status": "error"}, status=400)

    return JsonResponse({"status": "error"}, status=405)

def crear_usuario(request):
    pass

def banear_usuario(request, id):
    pass

def desbanear_usuario(request, id):
    pass

def enviar_correo(request, id):
    pass
