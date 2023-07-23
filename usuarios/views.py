from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from .forms import SolicitanteCreationForm
from administracion.models import UsuariosBaneados
from django.contrib import messages
from usuarios.models import Solicitante, Administrador
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, smart_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives


def not_authenticated(user):
    return not user.is_authenticated

@user_passes_test(not_authenticated, login_url='index', redirect_field_name=None)
def login_view(request):
    """
    View function for handling user login.

    This function handles the login process for users. It validates the login form, authenticates the user,
    and redirects them to the appropriate page based on their role (staff or solicitante). If the login is not
    successful, error messages are displayed.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object for rendering the login form or redirecting to the appropriate page.
    """
    if request.method == 'POST':
        email = request.POST.get('correo')
        password = request.POST.get('password')

        if not email or not password:
            return render(request, 'login.html', {'error': 'Por favor, complete todos los campos'})
        
        usuarioBan = Solicitante.objects.filter(email=email)
        usuarioBan = UsuariosBaneados.objects.filter(usuario__in=usuarioBan)
        if usuarioBan:
            return render(request, 'login.html', {'error': 'Lo sentimos, no puedes iniciar sesión en el sistema.'})
        

        user = authenticate(request, email=email, password=password)
        
        if not user.is_active:
            return render(request, 'login.html', {'error': 'Tu cuenta no esta activada, revisa tu correo electronico y activa tu cuenta'})


        if user is not None:
            try:
                if user.is_staff:
                    admin_user = Administrador.objects.get(pk=user.pk)
                    user_status = admin_user.estatus
                else:
                    solicitante_user = Solicitante.objects.get(pk=user.pk)
                    user_status = solicitante_user.estatus
            except (Administrador.DoesNotExist, Solicitante.DoesNotExist):
                return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
            
            if user_status == "Borrado":
                return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
            
            login(request, user)
            if user.is_staff:
                return redirect('administracion:panel')
            else:
                return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    else:
        # mostrar el formulario de inicio de sesión
        return render(request, 'login.html')


@user_passes_test(not_authenticated, login_url='index', redirect_field_name=None)
def register_solicitante(request):
    """
    View function for registering a new user (solicitante).
    
    This function handles the registration process for a new user (solicitante). It validates the registration form,
    creates a new user instance, sends an activation email to the user's provided email address, and displays a success
    message to the user. If there are any errors during the registration process, appropriate error messages are displayed.
    
    Parameters:
        request (HttpRequest): The HTTP request object.
        
    Returns:
        HttpResponse: The HTTP response object containing the rendered registration form or a redirect response.
    """
    if request.method == 'POST':
        beando = UsuariosBaneados.objects.filter(curp=request.POST.get('curp'))
        if beando:
            messages.error(request, 'Lo sentimos, no puedes registrarte en el sistema.')
            return redirect('usuarios:registro')
        
        form = SolicitanteCreationForm(request.POST)
        if form.is_valid():
            solicitante = form.save(commit=False)
            solicitante.is_active = False
            solicitante.backend = 'COSIAP.authentication.EmailBackend'
            solicitante.save()  # Guarda el usuario en la base de datos


            token = default_token_generator.make_token(solicitante)
            uid = urlsafe_base64_encode(force_bytes(solicitante.pk))
            current_site = get_current_site(request)
            mail_subject = 'Activa tu cuenta'
            message_plain = "Gracias por registrarte. Activa tu cuenta siguiendo el enlace enviado a tu correo."
            message_html = render_to_string('acc_active_email.html', {
                'user': solicitante,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            send_mail(
                mail_subject, 
                message_plain, 
                'info@mywebsite.com', 
                [solicitante.email],
                html_message=message_html
            )
            
            
            
            messages.success(request, 'Por favor confirma tu correo electrónico para completar el registro.')
            return redirect('usuarios:login')
        else:
            messages.error(request, 'Error en el registro. Por favor, verifica tus datos.')
    else:
        form = SolicitanteCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    """
    View function for logging out a user.

    This function logs out the currently authenticated user by clearing the user's session data.
    After logging out, the user is redirected to the home page.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object for redirection to the home page.
    """
    logout(request)
    return redirect('index')

def activate_account(request, uidb64, token):
    """
    View function for activating a user account.

    This function handles the activation process for a user account. It verifies the activation link provided
    by comparing the UID and token with the corresponding user in the database. If the verification is successful,
    the user's account is activated, and a success message is displayed. If the verification fails, an error message
    is displayed.

    Parameters:
        request (HttpRequest): The HTTP request object.
        uidb64 (str): The base64-encoded UID of the user.
        token (str): The activation token.

    Returns:
        HttpResponse: The HTTP response object for redirection or displaying a success/error message.
    """
    try:
        uid = smart_str(urlsafe_base64_decode(uidb64))
        solicitante = Solicitante.objects.get(pk=uid)
        if default_token_generator.check_token(solicitante, token):
            solicitante.is_active = True
            solicitante.save()
            messages.success(request, 'Tu cuenta ha sido activada, ahora puedes iniciar sesión.')
            return redirect('usuarios:login')
        else:
            messages.error(request, 'El enlace de activación es inválido.')
            return redirect('usuarios:registro')
    except (TypeError, ValueError, OverflowError, Solicitante.DoesNotExist):
        messages.error(request, 'El enlace de activación es inválido.')
        return redirect('usuarios:registro')
    
def reset_password(request):
    if request.method == 'POST':
        email = request.POST['correo']
        user = Solicitante.objects.filter(email=email)
        if user:
            user = user[0]
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            mail_subject = 'Restablecer tu contraseña'
            message_plain = "Haz clic en el enlace para restablecer tu contraseña."
            message_html = render_to_string('password_reset_send_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            email = EmailMultiAlternatives(mail_subject, message_plain, to=[user.email])
            email.attach_alternative(message_html, "text/html")
            email.send()
            messages.success(request, 'Te hemos enviado un correo con instrucciones para restablecer tu contraseña.')
        return redirect('usuarios:login')
    else:
       return render(request, 'recuperar_password.html')
    
def reset_confirm(request, uidb64, token):
    UserModel = get_user_model()

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST['password']
            confirm_password = request.POST['repassword']
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Tu contraseña ha sido actualizada.')
                return redirect('usuarios:login')
            else:
                messages.error(request, 'Las contraseñas no coinciden.')
        return render(request, 'password_reset_email.html')
    else:
        messages.error(request, 'El enlace de restablecimiento de contraseña no es válido.')
        return redirect('usuarios:login')