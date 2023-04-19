from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from .forms import SolicitanteCreationForm
from django.contrib import messages

def login(request):
    if request.method == 'POST':
        email = request.POST.get('correo')
        password = request.POST.get('password')

        if not email or not password:
            print("Mande error de que un campo no esta compleo")
            return render(request, 'login.html', {'error': 'Por favor, complete todos los campos'})

        user = authenticate(request, email=email, password=password)
        if user is not None:
            print("Intento hacer login")
            login(request, user)
            if user.is_staff:
                return redirect('administracion:index')
            else:
                return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    else:
        print("Regreso al formulario de login")
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
