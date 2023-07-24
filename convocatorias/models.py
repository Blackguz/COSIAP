from django.db import models
from usuarios.models import Solicitante
from django.utils import timezone

def solicitud_directory_path(instance, filename):
    """
    Generates a directory path for storing a document related to a support request.

    The directory path follows the pattern 'usuarios/{username}/solicitudes/{folder_name}/{filename}', 
    where 'folder_name' is a string formatted with the support request id, the username of the requester, 
    the current month and year, and the name of the modality.

    Args:
    instance (Model instance): The model instance the file is associated with. This should be an instance 
    of a model that has a foreign key relationship with the Solicitud model.
    filename (str): The original name of the file.

    Returns:
    str: The generated directory path.
    """
    # Formato: idSolicitud_username_mes_año_modalidad
    folder_name = '{0}_{1}_{2}_{3}_{4}'.format(
        instance.solicitud.pk,
        instance.solicitud.id_solicitante.username,
        timezone.now().month, 
        timezone.now().year, 
        instance.solicitud.id_modalidad.nombre
    )
    return 'usuarios/{0}/solicitudes/{1}/{2}'.format(instance.solicitud.id_solicitante.username, folder_name, filename)

class Estatus(models.Model):
    """
    Represents the status of a support request in the system.

    Each support request has an associated status which indicates the current state of the request 
    (e.g., 'pending', 'approved', 'rejected').

    Attributes:
    id_estatus (models.AutoField): The primary key for the status.
    nombre (models.CharField): The name of the status. Maximum length is 255 characters.
    """
    id_estatus = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Modalidad(models.Model):
    """
    Represents a modality of support requests in the system.

    Each modality has a name, a description, a list of requirements, a start and end date, 
    a budget and an associated status.

    Attributes:
    id_modalidad (models.AutoField): The primary key for the modality.
    nombre (models.CharField): The name of the modality. Maximum length is 255 characters.
    descripcion (models.TextField): The description of the modality.
    requisitos (models.TextField): The requirements for applying to this modality. 
                                   Default is 'sin requisitos'.
    fecha_inicio (models.DateField): The start date of the modality.
    fecha_fin (models.DateField): The end date of the modality.
    presupuesto (models.DecimalField): The budget allocated for this modality.
    estatus (models.ForeignKey): The status of the modality. 
                                 References the 'Estatus' model. It can be null.

    """
    id_modalidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    requisitos = models.TextField(null=True, blank=True, default='sin requisitos')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2)
    estatus = models.ForeignKey('convocatorias.Estatus', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Solicitud(models.Model):
    """
    Represents a support request within the system.

    Each request includes the amount requested and approved, the date of the request, 
    the status, the modality, the requester and any observations.

    Attributes:
    monto_solicitado (models.DecimalField): The amount of money requested. 
    monto_aprobado (models.DecimalField): The amount of money approved.
    fecha_solicitud (models.DateField): The date when the request was made.
    id_estatus (models.ForeignKey): The status of the request. References the 'Estatus' model.
    id_modalidad (models.ForeignKey): The modality of the request. References the 'Modalidad' model.
    id_solicitante (models.ForeignKey): The person who made the request. 
                                       References the custom 'Solicitante' model.
    observaciones (models.TextField): Additional notes about the request. This field is optional.
    id_solicitud (models.AutoField): The primary key for the request.
    """
    monto_solicitado = models.DecimalField(max_digits=10, decimal_places=2)
    monto_aprobado = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_solicitud = models.DateField()
    id_estatus = models.ForeignKey(Estatus, on_delete=models.CASCADE)
    id_modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE)
    id_solicitante = models.ForeignKey(Solicitante, on_delete=models.CASCADE) # Modelo personalizado 'Solicitante'
    observaciones = models.TextField(null=True, blank=True)
    id_solicitud = models.AutoField(primary_key=True)

    def __str__(self):
        return f'Solicitud {self.id_solicitud} - {self.id_solicitante.username}'

class DocumentoSolicitud(models.Model):
    """
    Represents a document associated with a request within the system.

    Each document is linked to a specific request and has a file associated with it.

    Attributes:
    solicitud (models.ForeignKey): The request to which the document is linked. 
                                   References the 'Solicitud' model.
    documento (models.FileField): The file associated with the document. 
                                  The file path is determined by the 'solicitud_directory_path' function.
    """
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='documentos')
    documento = models.FileField(upload_to=solicitud_directory_path)

    def __str__(self):
        nombre = self.documento.name.split('/')[-1]
        return f'Documento {self.id} - {nombre}'

class Formulario(models.Model):
    """
    Represents a form associated with a specific modality within the system.

    Each form is linked to a specific modality and has a name and status.

    Attributes:
    id_formulario (models.AutoField): The primary key for the form.
    id_modalidad (models.ForeignKey): The modality to which the form is linked. 
                                      References the 'Modalidad' model.
    nombre (models.CharField): The name of the form.
    estatus (models.ForeignKey): The status of the form. References the 'Estatus' model from the 'convocatorias' app.
    """
    id_formulario = models.AutoField(primary_key=True)
    id_modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255, default='sin nombre')
    estatus = models.ForeignKey('convocatorias.Estatus', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Formulario {self.id_formulario} - {self.id_modalidad.nombre}'

class AtributosFormulario(models.Model):
    """
    Represents an attribute of a form within the system.

    Each attribute is linked to a specific form and has a name, attribute type, and a boolean that indicates if it's a document.

    Attributes:
    TIPO_OPCIONES (list): A list of tuples that defines the available attribute types. 
                          The options include 'Texto', 'Numero', 'Fecha', 'Documento', and 'Telefono'.
    id_atributos_formularios (models.AutoField): The primary key for the form attribute.
    id_formulario (models.ForeignKey): The form to which the attribute is linked. 
                                       References the 'Formulario' model.
    nombre (models.CharField): The name of the form attribute.
    tipo_atributo (models.CharField): The type of attribute. Its value must be one of the options defined in 'TIPO_OPCIONES'.
    es_documento (models.BooleanField): A boolean value that indicates if the attribute is a document.
    """
    TIPO_OPCIONES = [
        ('Texto', 'Texto'),
        ('Numero', 'Numero'),
        ('Fecha', 'Fecha'),
        ('Documento', 'Documento'),
        ('Telefono', 'Telefono'),
    ]
    id_atributos_formularios = models.AutoField(primary_key=True)
    id_formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=85)
    tipo_atributo = models.CharField(max_length=15, choices=TIPO_OPCIONES)
    es_documento = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nombre} - {self.tipo_atributo}'

