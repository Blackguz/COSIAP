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
from .forms import EmailForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
import json
import os
from decimal import Decimal

# Create your views here.

@login_required
@staff_member_required
def panel_administracion(request):
    """
    View function for the administration panel.

    This function provides an administration panel with various statistics and counts related to the requests
    made in the system. It requires the user to be authenticated and staff member.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered administration panel with statistics and counts.
    """
    # Obtenemos el número de solicitudes por nivel de estudios
    estudios_nivel = get_solicitudes_por_nivel()

    # Agregar conteo de género por solicitud
    generos = get_generos_solicitantes()

    # Contamos todas las solicitudes
    solicitudes_autorizado = Solicitud.objects.filter(id_estatus=6).count()
    solicitudes_en_proceso = (
        Solicitud.objects.filter(id_estatus=2).count()
        + Solicitud.objects.filter(id_estatus=1).count()
        + Solicitud.objects.filter(id_estatus=3).count()
        + Solicitud.objects.filter(id_estatus=4).count()
    )

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
    """
    View function for displaying a list of active users.

    This function retrieves a list of active users (Solicitante) excluding those with the status "Eliminado"
    and those who have been banned. It then renders a template to display the list of active users.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered template with the list of active users.
    """
    estatus_eliminado = get_object_or_404(Estatus, id_estatus=7)
    baneados = UsuariosBaneados.objects.all()
    usuarios = Solicitante.objects.exclude(estatus=estatus_eliminado)
    usuarios = usuarios.exclude(id__in=baneados.values_list('usuario', flat=True))
    context = {
        "usuarios": usuarios
    }
    return render(request, "lista_usuarios.html", context)


@login_required
@staff_member_required
def eliminar_usuario(request, id):
    """
    View function for deleting a user.

    This function handles the process of deleting a user (either an Administrador or Solicitante) from the system.
    It updates the user's email, is_active, username, and estatus to mark the user as "eliminado". The function then
    redirects to the appropriate page depending on the type of user deleted (administrador or solicitante).

    Parameters:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the user to be deleted.

    Returns:
        HttpResponse: The HTTP response object for redirection to the appropriate page or rendering a confirmation template.
    """
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


@login_required
@staff_member_required
def editar_usuario(request, id):
    """
    View function for editing user information.

    This function handles the process of editing a user's (Solicitante) information. It expects a POST request with
    JSON data containing the updated user information. The user information is then updated in the database.

    Parameters:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the user (Solicitante) to be edited.

    Returns:
        JsonResponse: The JSON response object with the status of the edit operation (success or error).
    """
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


@login_required
@staff_member_required
def crear_usuario(request):
    """
    View function for creating a new user (Solicitante).

    This function handles the process of creating a new user (Solicitante) in the system. It expects a POST request
    containing the user registration form data. If the form data is valid, a new user is created and saved to the
    database. Otherwise, appropriate error messages are displayed.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object for rendering the user registration form or redirecting to the user list page.
    """
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


@login_required
@staff_member_required
def crear_administrador(request):
    """
    View function for creating a new administrator.

    This function handles the process of creating a new administrator in the system. It expects a POST request
    containing the administrator's information through the 'AdministradorForm'. If the form data is valid, a new
    administrator is created and saved to the database. The administrator is also assigned staff privileges by setting
    'is_staff' to True. If the form data is invalid, the form with error messages is displayed.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object for rendering the administrator creation form or redirecting to the administrator list page.
    """
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
    """
    View function for displaying a list of administrators.

    This function retrieves a list of administrators (objects of the 'Administrador' model) excluding those with
    the status "7" (eliminado) from the database. It then renders a template to display the list of administrators.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object for rendering the template with the list of administrators.
    """
    administradores = Administrador.objects.exclude(estatus='7')
    context = {
        "administradores": administradores
    }
    return render(request, "lista_administradores.html", context)


@login_required
@staff_member_required
def editar_administrador(request, id):
    """
    View function for editing administrator information.

    This function handles the process of editing an administrator's information. It expects a POST request with JSON
    data containing the updated administrator information. The administrator's information is then updated in the
    database.

    Parameters:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the administrator to be edited.

    Returns:
        JsonResponse: The JSON response object with the status of the edit operation (success or error).
    """
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
    """
    View function for banning a user.

    This function handles the process of banning a user (Solicitante) from the system. It takes the ID of the user to be
    banned as a parameter. If the user is already banned, an error message is displayed. Otherwise, the user is banned,
    and a new 'UsuariosBaneados' object is created and saved to the database. The user is also deactivated ('is_active'
    set to False) to prevent them from logging in.

    Parameters:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the user (Solicitante) to be banned.

    Returns:
        HttpResponse: The HTTP response object for redirecting to the user list page after banning the user.
    """
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
    """
    View function for unbanning a user.

    This function handles the process of unbanning a user (Solicitante) who has been previously banned. It takes the ID
    of the 'UsuariosBaneados' object representing the banned user as a parameter. If the user is found in the list of
    banned users, the user is unbanned (the 'UsuariosBaneados' object is deleted). A success message is displayed
    confirming the unban. If the user is not found in the list of banned users, an error message is displayed.

    Parameters:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the 'UsuariosBaneados' object representing the banned user.

    Returns:
        HttpResponse: The HTTP response object for redirecting to the banned users list page after unbanning the user.
    """
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
    """
    View function for sending an email to a user.

    This function handles the process of sending an email to a specific user (Solicitante). It expects the ID of the user
    as a parameter. If the request method is POST, it sends the email using the data from the 'EmailForm'. The email is
    sent to the user's email address and contains the subject and message provided in the form. Both plain text and HTML
    versions of the email are created to support different email clients. After sending the email, a success message is
    displayed. If the request method is not POST, it renders the 'EmailForm' to compose the email.

    Parameters:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the user (Solicitante) to whom the email will be sent.

    Returns:
        HttpResponse: The HTTP response object for redirecting to the panel page after sending the email or rendering the email composition form.
    """
    user = get_object_or_404(Solicitante, id=id)
    current_site = get_current_site(request)

    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            current_site = get_current_site(request)
            mail_subject = form.cleaned_data.get('asunto')
            message_plain = form.cleaned_data.get('mensaje')
            message_html = render_to_string('correo_template.html', {
                'user': user,
                'domain': current_site.domain,
                'mensaje': message_plain  # Aquí se cambió 'message' a 'mensaje'
            })
            email = EmailMultiAlternatives(mail_subject, message_plain, to=[user.email])
            email.attach_alternative(message_html, "text/html")
            email.send()
            messages.success(request, 'Correo enviado con exito!')
            return redirect('administracion:panel')
    else:
        form = EmailForm()

    return render(request, 'enviar_correo.html', {'form': form, 'usuario':user})

@login_required
@staff_member_required
def lista_modalidades(request):
    """
    View function for displaying a list of modalities.

    This function retrieves a list of modalities (objects of the 'Modalidad' model) excluding those with the status "7"
    (eliminado) from the database. It then renders a template to display the list of modalities.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object for rendering the template with the list of modalities.
    """
    modalidades = Modalidad.objects.exclude(estatus='7')
    context = {
        "modalidades": modalidades
    }
    return render(request, "lista_modalidades.html", context)

@login_required
@staff_member_required
def crear_modalidad(request):
    """
    View function for creating a new modality.

    This function handles the process of creating a new modality in the system. It expects a POST request containing the
    modality form data through the 'ModalidadForm'. If the form data is valid, a new modality is created and saved to
    the database. Otherwise, appropriate error messages are displayed.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object for rendering the modality creation form or redirecting to the modality list page.
    """
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
    """
    View function for editing modality information.

    This function handles the process of editing modality information. It expects a POST request with JSON data
    containing the updated modality information. The modality to be edited is identified by its 'id_modalidad' parameter.
    If the request method is POST, the modality information is updated in the database based on the provided JSON data.
    If the update is successful, a success JSON response is returned. If there is an error in the update, an error JSON
    response is returned. If the request method is not POST, an error JSON response with status 405 (Method Not Allowed)
    is returned.

    Parameters:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the modality to be edited.

    Returns:
        JsonResponse: The JSON response object with the status of the edit operation (success or error).
    """
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
    """
    View function for displaying a list of forms.

    This function handles the process of displaying a list of forms (objects of the 'Formulario' model) excluding those
    with the status "7" (eliminado) from the database. It requires the user to be logged in and have staff permissions
    to access the list of forms. The function retrieves all attributes of the forms using the 'AtributosFormulario' model.
    The forms and their attributes are then passed to the template for rendering.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object for rendering the template with the list of forms and their attributes.
    """
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
    """
    View function for deleting a modality.

    This function handles the process of deleting a modality from the system. It expects the ID of the modality to be
    deleted as a parameter. If the modality is already marked as deleted (status='7'), an error message is displayed
    and the function redirects to the modality list page. Otherwise, the modality's status is set to '7' (eliminado),
    and the modality is saved to the database. A success message is displayed, and the function redirects to the
    modality list page.

    Parameters:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the modality to be deleted.

    Returns:
        HttpResponse: The HTTP response object for redirecting to the modality list page.
    """
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
    """
    View function for updating a form and its attributes.

    This function handles the process of updating a form and its attributes in the system. It expects a POST request
    containing JSON data with the form and attribute information to be updated. The form to be updated is identified
    by its 'id_formulario' parameter. The function first updates the form's name. Then, it updates each attribute's name,
    type, and document flag based on the provided JSON data. If the update is successful, a success JSON response is
    returned. If there is an error in the update, an error JSON response is returned.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: The JSON response object with the status of the update operation (success or error).
    """
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
    """
    View function for creating a new form.

    This function handles the process of creating a new form in the system. It uses a formset to handle multiple form
    attributes (objects of the 'AtributosFormulario' model) associated with the form. The function expects a POST
    request with form data for the formset and the name and ID of the modality for the new form. If the form data is
    valid, a new form is created and saved to the database along with its associated attributes. Otherwise, appropriate
    error messages are displayed.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object for rendering the form creation form or redirecting to the form list page.
    """
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
    """
    View function for deleting a form and its attributes.

    This function handles the process of deleting a form and its associated attributes from the system. It expects the
    ID of the form to be deleted as a parameter. The function first deletes all attributes (objects of the
    'AtributosFormulario' model) associated with the form. Then, it deletes the form itself. If the deletion is
    successful, a success message is displayed, and the function redirects to the form list page. If the form is already
    deleted or not found, an error message is displayed, and the function also redirects to the form list page.

    Parameters:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the form to be deleted.

    Returns:
        HttpResponse: The HTTP response object for redirecting to the form list page.
    """
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
    """
    View function for displaying deleted modalities.

    This function handles the process of displaying modalities that have been marked as deleted (status='7') in the
    system. It retrieves the 'Estatus' object representing the deleted status using the ID '7'. Then, it retrieves all
    modalities that have the deleted status. The retrieved data is passed to the template for rendering.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object for rendering the template with the list of deleted modalities.
    """
    estatus_eliminado = get_object_or_404(Estatus, id_estatus=7)
    modalidades_eliminadas = Modalidad.objects.filter(estatus=estatus_eliminado)
    data = {
        'modalidades_eliminadas': modalidades_eliminadas
    }
    
    return render(request, 'papelera_modalidades.html', data)

@login_required
@staff_member_required
def restaurar_modalidad(request, id):
    """
    View function for restoring a deleted modality.

    This function handles the process of restoring a modality that has been marked as deleted (status='7') in the
    system. It retrieves the 'Estatus' object representing the deleted status using the ID '7' and the modality object
    with the specified ID. If the modality's status is not '7' (deleted), it means the modality is not deleted, and an
    error message is displayed. Otherwise, the modality's status is set to 'None' (null) to indicate that it is no
    longer deleted, and the changes are saved to the database. A success message is displayed, and the function redirects
    to the page displaying deleted modalities.

    Parameters:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the modality to be restored.

    Returns:
        HttpResponse: The HTTP response object for redirecting to the page displaying deleted modalities.
    """
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
    """
    View function for displaying deleted users.

    This function handles the process of displaying users (both 'Solicitante' and 'Administrador') who have been marked
    as deleted (status='7') in the system. It retrieves the 'Estatus' object representing the deleted status using the
    ID '7'. Then, it retrieves all 'Solicitante' objects and 'Administrador' objects that have the deleted status. The
    retrieved data is combined into a list of deleted users and passed to the template for rendering.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object for rendering the template with the list of deleted users.
    """
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
    """
    View function for restoring a deleted user.

    This function handles the process of restoring a user ('Solicitante' or 'Administrador') that has been marked as
    deleted (status='7') in the system. It retrieves the 'User' model object based on the ID provided and the 'Estatus'
    object representing the deleted status using the ID '7'. If the user is an 'Administrador', the function restores an
    'Administrador', and if the user is a 'Solicitante', the function restores a 'Solicitante'. The user's status is set
    to 'None' (null) to indicate that the user is no longer deleted, and the changes are saved to the database. A success
    message is displayed, and the function redirects to the page displaying deleted users. If the user is not deleted or
    not found, an error message is displayed, and the function also redirects to the page displaying deleted users.

    Parameters:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the user to be restored.

    Returns:
        HttpResponse: The HTTP response object for redirecting to the page displaying deleted users.
    """
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
    """
    View function for displaying a list of banned users.

    This function retrieves all the 'UsuariosBaneados' objects from the database, representing the banned users.
    It passes the retrieved data to the 'papelera_baneados.html' template for rendering.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object for rendering the template with the list of banned users.
    """
    baneados = UsuariosBaneados.objects.all()
    data = {
        'baneados':baneados
    }
    return render(request, 'papelera_baneados.html', data)

@login_required
@staff_member_required
def solicitudes_apoyos_nuevas(request):
    """
    View function for displaying new support requests.

    This function retrieves all the support requests ('Solicitud') that have the status of 'Documentación incompleta',
    'Pendiente', or 'Documentación completa' from the database. It organizes the retrieved data into a list of dictionaries
    containing each support request and its associated documents. The data is then passed to the 'solicitudes_apoyos_nuevas.html'
    template for rendering.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object for rendering the template with the list of new support requests.
    """
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
    """
    View function for downloading a specific document.

    This function handles the process of downloading a specific document associated with a support request ('Solicitud').
    It retrieves the 'DocumentoSolicitud' object with the given primary key (ID) from the database. If the document's file
    path exists, the function returns a 'FileResponse' with the document file opened in binary read mode. The 'FileResponse'
    forces the document to be downloaded by specifying the content type as 'application/force-download'. If the document does
    not exist or cannot be found, the function raises an HTTP 404 error.

    Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key (ID) of the document to be downloaded.

    Returns:
        FileResponse: The HTTP response object for downloading the document file.
        Http404: If the document with the given primary key does not exist.
    """
    documento = get_object_or_404(DocumentoSolicitud, pk=pk)
    if os.path.exists(documento.documento.path):
        return FileResponse(open(documento.documento.path, 'rb'), content_type='application/force-download')
    raise Http404

@login_required
@staff_member_required
def cambiar_estado(request, estado, solicitud):
    """
    View function for changing the status of a support request ('Solicitud').

    This function handles the process of changing the status of a support request to a specified state represented by its ID.
    It retrieves the 'Estatus' object corresponding to the state with the given ID ('estado') and the 'Solicitud' object
    with the given ID ('solicitud') from the database. If the support request already has the specified status, the function
    returns an error message. Otherwise, it updates the status of the support request to the specified state. The function then
    saves the updated 'Solicitud' object in the database and displays a success message.

    Parameters:
        request (HttpRequest): The HTTP request object.
        estado (int): The primary key (ID) of the target status to change to.
        solicitud (int): The primary key (ID) of the support request to change its status.

    Returns:
        HttpResponseRedirect: The HTTP redirect response object to the 'panel' view after the status is changed.
    """

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
    """
    View function for updating a support request ('Solicitud').

    This function handles the process of updating a support request identified by its ID ('id').
    It retrieves the 'Solicitud' object with the given ID from the database. The function then validates and processes
    the updated data from the HTTP POST request. It checks the provided 'monto_aprobado' (approved amount) and 'observaciones'
    (observations) for validity and constraints. If the provided 'monto_aprobado' is greater than the budget allocated for the
    corresponding 'Modalidad', the function displays an error message. If the provided 'monto_aprobado' or 'modalidad' is empty,
    the function also displays an error message. Otherwise, the function updates the 'Solicitud' object with the new data,
    saves it in the database, and displays a success message.

    Parameters:
        request (HttpRequest): The HTTP request object.
        id (int): The primary key (ID) of the support request ('Solicitud') to be updated.

    Returns:
        HttpResponseRedirect: The HTTP redirect response object to the 'panel' view after the update is completed.
    """

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
    """
    View function for displaying support requests in process ('En proceso de análisis' and 'Aceptado').

    This function retrieves all support requests ('Solicitud') that are in the process of analysis or have been accepted
    ('En proceso de análisis' or 'Aceptado'). It fetches the 'Solicitud' objects with the corresponding 'Estatus' objects
    from the database and organizes them with their associated documents.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered 'solicitudes_apoyos_proceso.html' template.
    """
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
    """
    View function for displaying approved support requests ('Aceptado').

    This function retrieves all support requests ('Solicitud') that have been approved ('Aceptado'). It fetches the 
    'Solicitud' objects with the corresponding 'Estatus' object ('Aceptado') from the database and organizes them with 
    their associated documents.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered 'solicitudes_apoyos_autorizadas.html' template.
    """
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
    """
    View function for displaying finalized support requests ('Finalizada').

    This function retrieves all support requests ('Solicitud') that have been marked as finalized ('Finalizada'). It fetches 
    the 'Solicitud' objects with the corresponding 'Estatus' object ('Finalizada') from the database and organizes them with 
    their associated documents.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered 'solicitudes_apoyos_finalizadas.html' template.
    """
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