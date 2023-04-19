from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from .forms import SolicitanteCreationForm
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('correo')
        password = request.POST.get('password')

        if not email or not password:
            return render(request, 'login.html', {'error': 'Por favor, complete todos los campos'})

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('administracion:panel')
            else:
                return redirect('COSIAP:index')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    else:
        # mostrar el formulario de inicio de sesión
        return render(request, 'login.html')

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
