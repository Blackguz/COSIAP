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
    """
    View for displaying a list of SolicitudSoporte objects with the estado 'EN' (en espera).

    This view extends the ListView class provided by Django. It is used to render a list of SolicitudSoporte objects
    where the 'estado' field is set to 'EN' (en espera). The template used for rendering is 'solicitud_soporte.html'.

    Attributes:
        model (class): The model class associated with this view, in this case, the SolicitudSoporte model.
        template_name (str): The name of the template used for rendering the list of SolicitudSoporte objects.

    Methods:
        get_queryset(): Returns the queryset of SolicitudSoporte objects to be displayed in the view.
    """
    model = SolicitudSoporte
    template_name = 'solicitud_soporte.html'

    def get_queryset(self):
        return SolicitudSoporte.objects.filter(estado='EN')

@method_decorator(staff_member_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class SolicitudesEnAtencionView(ListView):
    """
    View for displaying a list of SolicitudSoporte objects with the estado 'EA' (en atención).

    This view extends the ListView class provided by Django. It is used to render a list of SolicitudSoporte objects
    where the 'estado' field is set to 'EA' (en atención). The template used for rendering is 'solicitudes_en_atencion.html'.

    Attributes:
        model (class): The model class associated with this view, in this case, the SolicitudSoporte model.
        template_name (str): The name of the template used for rendering the list of SolicitudSoporte objects.

    Methods:
        get_queryset(): Returns the queryset of SolicitudSoporte objects to be displayed in the view.
    """
    model = SolicitudSoporte
    template_name = 'solicitudes_en_atencion.html'

    def get_queryset(self):
        return SolicitudSoporte.objects.filter(estado='EA')

@method_decorator(staff_member_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class SolicitudesAtendidasView(ListView):
    """
    View for displaying a list of SolicitudSoporte objects with the estado 'AT' (atendidas).

    This view extends the ListView class provided by Django. It is used to render a list of SolicitudSoporte objects
    where the 'estado' field is set to 'AT' (atendidas). The template used for rendering is 'solicitudes_atendidas.html'.

    Attributes:
        model (class): The model class associated with this view, in this case, the SolicitudSoporte model.
        template_name (str): The name of the template used for rendering the list of SolicitudSoporte objects.

    Methods:
        get_queryset(): Returns the queryset of SolicitudSoporte objects to be displayed in the view.
    """
    model = SolicitudSoporte
    template_name = 'solicitudes_atendidas.html'

    def get_queryset(self):
        return SolicitudSoporte.objects.filter(estado='AT')

@login_required
@staff_member_required
def cambiar_estado_solicitud(request, id_solicitud, nuevo_estado):
    """
    View function to change the estado of a SolicitudSoporte object.

    This function is responsible for changing the estado of a SolicitudSoporte object based on the provided nuevo_estado
    parameter. It takes the id_solicitud to identify the specific SolicitudSoporte object to update. After updating the
    estado, it redirects the user to the corresponding page depending on the nuevo_estado.

    Args:
        request (HttpRequest): The HTTP request object.
        id_solicitud (int): The ID of the SolicitudSoporte object to update.
        nuevo_estado (str): The new estado to set for the SolicitudSoporte object.

    Returns:
        HttpResponseRedirect: A redirect to the corresponding page based on the nuevo_estado.

    Raises:
        Http404: If the SolicitudSoporte object with the specified id_solicitud does not exist.

    """
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
    """
    View class for creating a new SolicitudSoporte object.

    This view class is used to create a new SolicitudSoporte object using the SolicitudSoporteForm form. When the form is
    valid, the SolicitudSoporte object is saved with the estado set to 'EN' (En espera) and a success message is shown
    to the user. Then, the user is redirected to the success_url.

    Attributes:
        model (class): The model class associated with this view (SolicitudSoporte).
        form_class (class): The form class to use for creating a new SolicitudSoporte object (SolicitudSoporteForm).
        success_url (str): The URL to redirect the user after a successful form submission (reverse_lazy('index')).

    Methods:
        form_valid(form): Override the form_valid method to set the estado and show a success message.

    """
    model = SolicitudSoporte
    form_class = SolicitudSoporteForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.estado = 'EN'
        messages.success(self.request, 'Solicitud de apoyo enviada')
        return super().form_valid(form)
