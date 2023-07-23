from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse, FileResponse, Http404
from convocatorias.models import Solicitud, Modalidad, Formulario, AtributosFormulario, DocumentoSolicitud
from convocatorias.forms import ModalidadForm, FormularioForm, AtributoFormularioForm
from soporte.models import SolicitudSoporte
from django.forms.formsets import formset_factory
from usuarios.models import Solicitante, Administrador
from usuarios.forms import SolicitanteCreationForm, AdministradorForm
from administracion.models import UsuariosBaneados
from convocatorias.models import Estatus
from django.db.models import Q
from usuarios.forms import SolicitanteCreationForm
from .utils import get_solicitudes_por_nivel, get_generos_solicitantes
import json
import os
from decimal import Decimal

# Create your views here.

@login_required
@staff_member_required
def panel_administracion(request):
    # Obtenemos el número de solicitudes por nivel de estudios
    estudios_nivel = get_solicitudes_por_nivel()

    # Agregar conteo de género por solicitud
    generos = get_generos_solicitantes()
    
    # Contamos todas las solicitudes
    solicitudes_autorizado = Solicitud.objects.filter(id_estatus=6).count()
    print(solicitudes_autorizado)
    solicitudes_en_proceso = Solicitud.objects.filter(id_estatus=2).count() + Solicitud.objects.filter(id_estatus=1).count() + Solicitud.objects.filter(id_estatus=3).count() + Solicitud.objects.filter(id_estatus=4).count()
    
    # Obtenemos el numero de solicitudes de soporte tecnico pendientes
    solicitudes_soporte_tecnico = SolicitudSoporte.objects.filter(estado='EN').count()



    context = {
        "niveles_estudios": estudios_nivel[0],
        "solicitudes_por_nivel": estudios_nivel[1],
        "generos": [generos['Masculino'], generos['Femenino']],
        "solicitudes_autorizado": solicitudes_autorizado,
        "solicitudes_en_proceso": solicitudes_en_proceso,
        "soporte": solicitudes_soporte_tecnico
    }

    return render(request, "panel.html", context)

@login_required
@staff_member_required
def lista_usuarios(request):
    estatus_eliminado = get_object_or_404(Estatus, id_estatus=7)
    baneados = UsuariosBaneados.objects.all()
    usuarios = Solicitante.objects.exclude(estatus=estatus_eliminado)
    usuarios = usuarios.exclude(id__in=baneados.values_list('usuario', flat=True))
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
    usuario = get_object_or_404(Solicitante, id=id)
    try:
        baneado = UsuariosBaneados.objects.get(usuario=usuario)
        messages.error(request, 'El usuario ya se encuentra baneado!')
    except UsuariosBaneados.DoesNotExist:
        baneado = UsuariosBaneados.objects.create(usuario=usuario, curp=usuario.curp)
        baneado.save()
        usuario.is_active = False
        usuario.save()
        messages.success(request, 'Usuario baneado exitosamente!')

    return redirect('administracion:usuarios')

@login_required
@staff_member_required
def desbanear_usuario(request, id):
    usuario = get_object_or_404(UsuariosBaneados, id=id)
    if usuario:
        usuario.delete()
        messages.success(request, 'Usuario desbaneado exitosamente')
        return redirect('administracion:baneados')
    else:
        messages.error(request, 'El usuario no se encuentra en la lista de baneados')
        return redirect('administracion:baneados')
        

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
def editar_modalidad(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        modalidad = get_object_or_404(Modalidad, id_modalidad=id)

        
        modalidad.nombre = data.get("nombre")
        modalidad.presupuesto = data.get("presupuest_asignado")
        modalidad.fecha_inicio = data.get("fecha_inicio")
        modalidad.fecha_fin = data.get("fecha_fin")
        modalidad.descripcion = data.get("descripcion")
        modalidad.requisitos = data.get("requisitos")

        try:
            modalidad.save()
            return JsonResponse({"status": "success"}, status=200)
        except:
            return JsonResponse({"status": "error"}, status=400)

    return JsonResponse({"status": "error"}, status=405)




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
    if formulario:
        AtributosFormulario.objects.filter(id_formulario=formulario).delete()
        formulario.delete()
        messages.success(request, 'Formulario eliminado.')
        return redirect('administracion:lista_formularios')
    else:
        messages.error(request, 'El formulario ya ha sido eliminado.')
        return redirect('administracion:lista_formularios')
       
    
@login_required
@staff_member_required
def papelera_modalidades(request):
    estatus_eliminado = get_object_or_404(Estatus, id_estatus=7)
    modalidades_eliminadas = Modalidad.objects.filter(estatus=estatus_eliminado)
    data = {
        'modalidades_eliminadas': modalidades_eliminadas
    }
    
    return render(request, 'papelera_modalidades.html', data)

@login_required
@staff_member_required
def restaurar_modalidad(request, id):
    estatus_eliminado = get_object_or_404(Estatus, id_estatus=7)
    modalidad = get_object_or_404(Modalidad, id_modalidad=id)
    if modalidad.estatus != estatus_eliminado:
        messages.error(request, 'Esta modalidad no esta eliminado')
        return redirect('administracion:modalidades_eliminadas')
    else:
        modalidad.estatus= None
        modalidad.save()
        messages.success(request, 'Modalidad restaurada exitosamente!')
        return redirect('administracion:modalidades_eliminadas')
    
@login_required
@staff_member_required
def papelera_usuarios(request):
    User = get_user_model()
    estatus_eliminado = get_object_or_404(Estatus, id_estatus=7)
    solicitantes_eliminados = Solicitante.objects.filter(estatus=estatus_eliminado)
    administradores_eliminados = Administrador.objects.filter(estatus=estatus_eliminado)
    usuarios_eliminados = list(solicitantes_eliminados) + list(administradores_eliminados)
    data = {
        'usuarios_eliminados': usuarios_eliminados
    }
    return render(request, 'papelera_usuarios.html', data)

@login_required
@staff_member_required
def restaurar_usuario(request, id):
    User = get_user_model()
    usuario = get_object_or_404(User, id=id)
    estatus_eliminado = get_object_or_404(Estatus, id_estatus=7)
    if usuario.is_staff:
        usuario = Administrador.objects.get(pk=usuario.pk)
        messages.success(request, 'Administrador restauraro exitosamente!')
    else:
        usuario = Solicitante.objects.get(pk=usuario.pk)
        messages.success(request, 'Usuario restauraro exitosamente!')

    if usuario.estatus != estatus_eliminado:
        messages.error(request, 'El usuario no esta eliminado!')
        return redirect('administracion:papelera_usuarios')


    usuario.email = usuario.email.replace("_eliminado", "")
    usuario.is_active = True
    usuario.username = usuario.username.replace("_eliminado", "")
    usuario.estatus = None
    usuario.save()
    return redirect('administracion:papelera_usuarios')

@login_required
@staff_member_required
def lista_baneados(request):
    baneados = UsuariosBaneados.objects.all()
    data = {
        'baneados':baneados
    }
    return render(request, 'papelera_baneados.html', data)

@login_required
@staff_member_required
def solicitudes_apoyos_nuevas(request):
    pendiente_status = Estatus.objects.get(nombre='Pendiente')
    documentacion_incompleta_status = Estatus.objects.get(nombre='Documentación incompleta')
    documentacion_completa_status = Estatus.objects.get(pk=2)

    solicitudes_apoyos = Solicitud.objects.filter(Q(id_estatus=documentacion_completa_status) |Q(id_estatus=pendiente_status) | Q(id_estatus=documentacion_incompleta_status))

    solicitudes_data = []
    for solicitud in solicitudes_apoyos:
        documentos = solicitud.documentos.all()
        solicitudes_data.append({
            'solicitud': solicitud,
            'documentos': documentos
        })

    data = {
        'solicitudes_data': solicitudes_data
    }

    return render(request, 'solicitudes_apoyos_nuevas.html', data)

@login_required
@staff_member_required
def download_documento(request, pk):
    documento = get_object_or_404(DocumentoSolicitud, pk=pk)
    if os.path.exists(documento.documento.path):
        return FileResponse(open(documento.documento.path, 'rb'), content_type='application/force-download')
    raise Http404

@login_required
@staff_member_required
def cambiar_estado(request, estado, solicitud):

    estado_solicitud = get_object_or_404(Estatus, pk=estado)
    solicitud_obj = get_object_or_404(Solicitud, pk=solicitud)

    if solicitud_obj.id_estatus == estado_solicitud:
        messages.error(request, f'esta solicitud ya tiene el estado de {estado_solicitud.nombre}')
        return redirect('administracion:solicitudes_apoyos_nuevas')

    estado_nombre = estado_solicitud.nombre
    if estado_nombre == "Pendiente":
        solicitud_obj.id_estatus = get_object_or_404(Estatus, pk=1)
    elif estado_nombre == "Documentación completa":
        solicitud_obj.id_estatus = get_object_or_404(Estatus, pk=2)
    elif estado_nombre == "En proceso de análisis":
        solicitud_obj.id_estatus = get_object_or_404(Estatus, pk=3)
    elif estado_nombre == "Aceptado":
        solicitud_obj.id_estatus = get_object_or_404(Estatus, pk=4)
    elif estado_nombre == "Rechazado":
        solicitud_obj.id_estatus = get_object_or_404(Estatus, pk=5)
    elif estado_nombre == "Autorizado":
        solicitud_obj.id_estatus = get_object_or_404(Estatus, pk=6)
    elif estado_nombre == "Borrado":
        solicitud_obj.id_estatus = get_object_or_404(Estatus, pk=7)
    elif estado_nombre == "Documentación incompleta":
        solicitud_obj.id_estatus = get_object_or_404(Estatus, pk=8)
    elif estado_nombre == "Finalizada":
        solicitud_obj.id_estatus = get_object_or_404(Estatus, pk=9)
    else:
        messages.error(request, 'Ese estado no esta disponible')
        return redirect('administracion:panel')

    solicitud_obj.save()
    messages.success(request, f'Estado cambiado exitosamente a {estado_solicitud.nombre}')
    return redirect('administracion:panel')


@login_required
@staff_member_required
def actualizar_solicitud(request, id):
    solicitud_obj = get_object_or_404(Solicitud, pk=id)

    monto_aprobado = request.POST.get(f'monto_aprobado{id}')
    if monto_aprobado:
        monto_aprobado = Decimal(monto_aprobado.replace(',', ''))
    else:
        messages.error(request, 'Monto aprobado no puede estar vacío.')
        return redirect('administracion:panel')

    observaciones = request.POST.get(f'observaciones{id}')

    modalidad = solicitud_obj.id_modalidad
    if not modalidad:
        messages.error(request, 'La modalidad no puede estar vacía.')
        return redirect('administracion:panel')

    if monto_aprobado > modalidad.presupuesto:
        messages.error(request, 'El monto aprobado no puede ser mayor que el presupuesto de la modalidad.')
        return redirect('administracion:panel')

    solicitud_obj.monto_aprobado = monto_aprobado
    solicitud_obj.observaciones = observaciones
    solicitud_obj.save()

    messages.success(request, 'La solicitud ha sido actualizada exitosamente.')
    return redirect('administracion:panel')

@login_required
@staff_member_required
def solicitudes_apoyos_proceso(request):
    analisis_status = Estatus.objects.get(pk=3)
    aceptado_status = Estatus.objects.get(pk=4)

    solicitudes_apoyos = Solicitud.objects.filter(Q(id_estatus=analisis_status) | Q(id_estatus=aceptado_status))

    solicitudes_data = []
    for solicitud in solicitudes_apoyos:
        documentos = solicitud.documentos.all()
        solicitudes_data.append({
            'solicitud': solicitud,
            'documentos': documentos
        })

    data = {
        'solicitudes_data': solicitudes_data
    }

    return render(request, 'solicitudes_apoyos_proceso.html', data)

@login_required
@staff_member_required
def solicitudes_aprovadas(request):
    aprovado_status = Estatus.objects.get(pk=6)

    solicitudes_apoyos = Solicitud.objects.filter(Q(id_estatus=aprovado_status))

    solicitudes_data = []
    for solicitud in solicitudes_apoyos:
        documentos = solicitud.documentos.all()
        solicitudes_data.append({
            'solicitud': solicitud,
            'documentos': documentos
        })

    data = {
        'solicitudes_data': solicitudes_data
    }

    return render(request, 'solicitudes_apoyos_autorizadas.html', data)

@login_required
@staff_member_required
def solicitudes_finalizadas(request):
    aprovado_status = Estatus.objects.get(pk=9)

    solicitudes_apoyos = Solicitud.objects.filter(Q(id_estatus=aprovado_status))

    solicitudes_data = []
    for solicitud in solicitudes_apoyos:
        documentos = solicitud.documentos.all()
        solicitudes_data.append({
            'solicitud': solicitud,
            'documentos': documentos
        })

    data = {
        'solicitudes_data': solicitudes_data
    }

    return render(request, 'solicitudes_apoyos_finalizadas.html', data)