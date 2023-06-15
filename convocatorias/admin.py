from django.contrib import admin
from .models import Estatus, Modalidad, Solicitud, Formulario, AtributosFormulario, DocumentoSolicitud

admin.site.register(Estatus)
admin.site.register(Modalidad)
admin.site.register(Solicitud)
admin.site.register(Formulario)
admin.site.register(AtributosFormulario)
admin.site.register(DocumentoSolicitud)