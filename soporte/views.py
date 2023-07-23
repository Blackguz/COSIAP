from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect
from .models import SolicitudSoporte
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .models import SolicitudSoporte
from .forms import SolicitudSoporteForm
from django.contrib import messages
from django.urls import reverse_lazy


@method_decorator(staff_member_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class SolicitudesEnEsperaView(ListView):
    model = SolicitudSoporte
    template_name = 'solicitud_soporte.html'

    def get_queryset(self):
        return SolicitudSoporte.objects.filter(estado='EN')

@method_decorator(staff_member_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class SolicitudesEnAtencionView(ListView):
    model = SolicitudSoporte
    template_name = 'solicitudes_en_atencion.html'

    def get_queryset(self):
        return SolicitudSoporte.objects.filter(estado='EA')

@method_decorator(staff_member_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class SolicitudesAtendidasView(ListView):
    model = SolicitudSoporte
    template_name = 'solicitudes_atendidas.html'

    def get_queryset(self):
        return SolicitudSoporte.objects.filter(estado='AT')

@login_required
@staff_member_required
def cambiar_estado_solicitud(request, id_solicitud, nuevo_estado):
    solicitud = get_object_or_404(SolicitudSoporte, id=id_solicitud)

    if nuevo_estado == 'EN':
        solicitud.estado = nuevo_estado
        solicitud.save()
        messages.success(request, 'Solicitud en espera ahora!')
        return redirect('soporte:solicitudes_en_espera')
    elif nuevo_estado == 'EA':
        solicitud.estado = nuevo_estado
        solicitud.save()        
        messages.success(request, 'Solicitud en atencion ahora!')
        return redirect('soporte:solicitudes_atencion')
    elif nuevo_estado == 'AT':
        solicitud.estado = nuevo_estado
        solicitud.save()
        messages.success(request, 'Atencion finalizada con exito!')
        return redirect('soporte:solicitudes_atendidas')
    else:
        messages.error(request, 'El estado no esta disponible')
        return redirect('soporte:solicitudes_en_espera')

class CrearSolicitudView(CreateView):
    model = SolicitudSoporte
    form_class = SolicitudSoporteForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.estado = 'EN'
        messages.success(self.request, 'Solicitud de apoyo enviada')
        return super().form_valid(form)
