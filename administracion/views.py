from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from convocatorias.models import Solicitud, Modalidad, Formulario, AtributosFormulario
from convocatorias.forms import ModalidadForm, FormularioForm, AtributoFormularioForm
from django.forms.formsets import formset_factory
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
        area_enviar = True
        
        if usuario.is_staff:
            usuario = Administrador.objects.get(pk=usuario.pk)
            messages.success(request, 'Administrador eliminado exitosamente!')
        else:
            usuario = Solicitante.objects.get(pk=usuario.pk)
            messages.success(request, 'Usuario eliminado exitosamente!')
            area_enviar = False

        if usuario.estatus == estatus_eliminado:
            return redirect('administracion:usuarios')

        usuario.email = usuario.email + '_eliminado'
        usuario.is_active = False
        usuario.username = usuario.username + '_eliminado'
        usuario.estatus = estatus_eliminado
        usuario.save()

        if area_enviar:
            return redirect('administracion:administradores')
        else:
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

@login_required
@staff_member_required
def lista_formularios(request):
    formularios = Formulario.objects.exclude(estatus='7')
    # trae todos los atributos de los formularios sin el estatus de eliminado
    atributos = AtributosFormulario.objects.all()
    context = {
        "formularios": formularios
    }
    return render(request, "lista_formularios.html", context)

@login_required
@staff_member_required
def eliminar_modalidad(request, id):
    modalidad = get_object_or_404(Modalidad, id_modalidad=id)
    if modalidad.estatus == '7':
        messages.error(request, 'La modalidad ya se encuentra eliminada.')
        return redirect('administracion:modalidades')
    
    else:
        estatus = Estatus.objects.get(pk='7')
        modalidad.estatus = estatus
        modalidad.save()
        messages.success(request, 'La modalidad se ha eliminado correctamente.')
        return redirect('administracion:modalidades')

@login_required
@staff_member_required
def actualizar_formulario(request):
    if request.method == 'POST':
        # Parsear JSON
        data = json.loads(request.body)

        # Obtener el objeto Formulario
        formulario_id = data.get('id')
        formulario = get_object_or_404(Formulario, id_formulario=formulario_id)

        # Actualizar el Formulario
        formulario.nombre = data.get('nombre')
        formulario.save()

        # Obtener y actualizar los AtributosFormulario
        atributos_data = data.get('atributos')
        for atributo_data in atributos_data:
            atributo_id = atributo_data.get('id')
            atributo = get_object_or_404(AtributosFormulario, id_atributos_formularios=atributo_id)
            atributo.nombre = atributo_data.get('nombre')
            atributo.tipo_atributo = atributo_data.get('tipo_atributo')
            atributo.es_documento = atributo_data.get('es_documento')
            atributo.save()

        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error", "message": "Método no permitido."})

@login_required
@staff_member_required
def crear_formulario(request):
    AtributosFormset = formset_factory(AtributoFormularioForm, extra=1)
    modalidades = Modalidad.objects.exclude(estatus='7')
    if request.method == 'POST':
        formset = AtributosFormset(request.POST)
        nombre_formulario = request.POST.get('nombre')
        id_modalidad = request.POST.get('id_modalidad')
        print("nombre_formulario: ", nombre_formulario, "id_modalidad: ", id_modalidad)
        print(request.POST)
        
        if nombre_formulario and id_modalidad:
            modalidad = Modalidad.objects.get(pk=id_modalidad)
            formulario = Formulario.objects.create(nombre=nombre_formulario, id_modalidad=modalidad)
            formulario.save()

            if formset.is_valid():
                for form in formset:
                    if form.is_valid():
                        atributo = form.save(commit=False)
                        atributo.id_formulario = formulario  # Asignar el formulario al atributo
                        atributo.save()
                
                messages.success(request, 'Registro exitoso!')
                return redirect('administracion:lista_formularios')
            else:
                messages.error(request, 'Error en el registro. Por favor, verifica los datos.')
        else:
            messages.error(request, 'Error en el registro. Por favor, proporciona el nombre del formulario y la modalidad.')
    else:
        formset = AtributosFormset()
    
    return render(request, 'crear_formulario.html', {'formset': formset, 'modalidades': modalidades})

@login_required
@staff_member_required
def eliminar_formulario(request, id):
    formulario = get_object_or_404(Formulario, id_formulario=id)
    if formulario.estatus == '7':
        messages.error(request, 'El formulario ya ha sido eliminado.')
        return redirect('administracion:lista_formularios')
    else:
        AtributosFormulario.objects.filter(id_formulario=formulario).delete()
        estatus = Estatus.objects.get(pk='7')
        formulario.estatus = estatus
        formulario.save()
        messages.success(request, 'Formulario eliminado.')
        return redirect('administracion:lista_formularios')