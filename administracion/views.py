from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from convocatorias.models import Solicitud, Modalidad
from convocatorias.forms import ModalidadForm
from usuarios.models import Solicitante, Administrador
from usuarios.forms import SolicitanteCreationForm, AdministradorForm
from convocatorias.models import Estatus
from usuarios.forms import SolicitanteCreationForm
from .utils import get_solicitudes_por_nivel, get_generos_solicitantes
import json

# Create your views here.

@login_required
@staff_member_required
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

@login_required
@staff_member_required
def lista_usuarios(request):
    estatus_eliminado = get_object_or_404(Estatus, id_estatus=7)
    usuarios = Solicitante.objects.exclude(estatus=estatus_eliminado)
    context = {
        "usuarios": usuarios
    }
    return render(request, "lista_usuarios.html", context)

'''
Esta funcion sirve para eliminar un usuario, pero no lo elimina de la base de datos, solo 
cambia su estatus a eliminado y cambia su email, username y password para que no pueda
acceder al sistema.
'''
@login_required
@staff_member_required
def eliminar_usuario(request, id):
    User = get_user_model()
    if request.method == 'POST':
        usuario = get_object_or_404(User, id=id)
        estatus_eliminado = get_object_or_404(Estatus, id_estatus=7)
        if usuario.estatus == estatus_eliminado:
            return redirect('administracion:usuarios')
        
        if usuario.is_staff:
            admin_user = Administrador.objects.get(pk=usuario.pk)
            admin_user.estatus = estatus_eliminado
        else:
            solicitante_user = Solicitante.objects.get(pk=usuario.pk)
            solicitante_user.estatus = estatus_eliminado

        usuario.email = usuario.email + '_eliminado'
        usuario.is_active = False
        usuario.username = usuario.username + '_eliminado'
        usuario.save()

        if usuario.is_staff:
            admin_user.save()
        else:
            solicitante_user.save()

        return redirect('administracion:usuarios')
    else:
        # Renderizar una plantilla de confirmación de eliminación
        return render(request, 'confirmar_eliminacion.html', {'id': id})

'''
Esta funcion lo que hace es recuperar los datos enviados por ajax y los guarda en la base de datos
así actualizando al usuario solicitado.
'''
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

'''
Esta vista sirve para crear un usuario. Se utiliza el formulario SolicitanteCreationForm
para crear un usuario solicitante.
'''
@login_required
@staff_member_required
def crear_usuario(request):
    if request.method == 'POST':
        print(request.POST)
        form = SolicitanteCreationForm(request.POST)
        if form.is_valid():
            solicitante = form.save()
            messages.success(request, 'Registro exitoso!')
            return redirect('administracion:usuarios')
        else:
            messages.error(request, 'Error en el registro. Por favor, verifica los datos.')
    else:
        form = SolicitanteCreationForm()
    return render(request, 'crear_usuario.html', {'form': form})

'''
Esta vista sirve para crear un administrador. Se utiliza el formulario AdministradorForm
'''
@login_required
@staff_member_required
def crear_administrador(request):
    if request.method == 'POST':
        form = AdministradorForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True
            user.save()
            # Puedes agregar un mensaje de éxito aquí usando el paquete 'messages' de Django
            return redirect('administracion:administradores')
        else:
            # Si hay errores en el formulario, se mostrarán en la plantilla
            return render(request, 'crear_administrador.html', {'form': form})
    else:
        form = AdministradorForm()
        return render(request, 'crear_administrador.html', {'form': form})

@login_required
@staff_member_required
def lista_administradores(request):
    administradores = Administrador.objects.exclude(estatus='7')
    context = {
        "administradores": administradores
    }
    return render(request, "lista_administradores.html", context)

'''
Vista que nos permite editar un administrador. Se trae al objeto administrador de la base de datos
y se edita directamente.
'''
@login_required
@staff_member_required
def editar_administrador(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        usuario = get_object_or_404(Administrador, id=id)

        usuario.first_name = data.get("nombre")
        usuario.apellido_materno = data.get("apellido_materno")
        usuario.apellido_paterno = data.get("apellido_paterno")
        usuario.telefono_celular = data.get("telefono_celular")
        usuario.nivel_acceso = data.get("nivel_acceso")
        try:
            usuario.save()
            return JsonResponse({"status": "success"}, status=200)
        except:
            return JsonResponse({"status": "error"}, status=400)

@login_required
@staff_member_required
def banear_usuario(request, id):
    pass

@login_required
@staff_member_required
def desbanear_usuario(request, id):
    pass

@login_required
@staff_member_required
def enviar_correo(request, id):
    pass


@login_required
@staff_member_required
def lista_modalidades(request):
    modalidades = Modalidad.objects.exclude(estatus='7')
    context = {
        "modalidades": modalidades
    }
    return render(request, "lista_modalidades.html", context)

@login_required
@staff_member_required
def crear_modalidad(request):
    if request.method == 'POST':
        form = ModalidadForm(request.POST)
        if form.is_valid():
            modalidad = form.save()
            messages.success(request, 'Registro exitoso!')
            return redirect('administracion:modalidades')
        else:
            messages.error(request, 'Error en el registro. Por favor, verifica los datos.')
    else:
        form = ModalidadForm()
    return render(request, 'crear_modalidad.html', {'form': form})
