from django.shortcuts import render, redirect
from convocatorias.forms import SolicitudApoyoForm
# Create your views here.

def index(request):
    if request.method == 'POST':
        formulario_solicitud = SolicitudApoyoForm(request.POST)
        if formulario_solicitud.is_valid():
            formulario_solicitud.save()
            return redirect('index')
    else:
        formulario_solicitud = SolicitudApoyoForm()
    return render(request, 'index.html', {'form': formulario_solicitud})
