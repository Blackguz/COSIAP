from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from .forms import SolicitanteCreationForm
from django.contrib import messages
from usuarios.models import Solicitante, Administrador


def not_authenticated(user):
    return not user.is_authenticated

@user_passes_test(not_authenticated, login_url='index', redirect_field_name=None)
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('correo')
        password = request.POST.get('password')

        if not email or not password:
            return render(request, 'login.html', {'error': 'Por favor, complete todos los campos'})

        user = authenticate(request, email=email, password=password)
        
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
    if request.method == 'POST':
        form = SolicitanteCreationForm(request.POST)
        if form.is_valid():
            solicitante = form.save()
            login(request)
            messages.success(request, 'Registro exitoso. Bienvenido/a!')
            return redirect('index')
        else:
            messages.error(request, 'Error en el registro. Por favor, verifica tus datos.')
    else:
        form = SolicitanteCreationForm()
    return render(request, 'register.html', {'form': form})
