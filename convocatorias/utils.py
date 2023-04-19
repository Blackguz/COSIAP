import os
from django.utils import timezone

def user_directory_path(instance, filename):
    user = instance.id_solicitante
    solicitud = instance.id
    solicitud_nombre = instance.nombre
    
    # Obtener la instancia de la modalidad asociada con la solicitud
    modalidad = instance.id_modalidad

    # Obtener las fechas de inicio y fin de la modalidad
    fecha_inicio = modalidad.fecha_inicio.strftime("%Y%m%d")
    fecha_fin = modalidad.fecha_fin.strftime("%Y%m%d")
    
    # Crear la carpeta para la solicitud
    folder = f"{user.id}_{solicitud_nombre}_{fecha_inicio}_{fecha_fin}"
    
    # Crear el nombre del archivo
    file_name = f"CURP_{user.first_name}_{user.last_name}_{timezone.now().strftime('%Y%m%d')}.{filename.split('.')[-1]}"

    return os.path.join(f"{user.id}/documentos/{folder}/", file_name)
