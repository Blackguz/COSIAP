from django.shortcuts import render

# Create your views here.
def panel_administracion(request):
    return render(request, 'panel.html')
