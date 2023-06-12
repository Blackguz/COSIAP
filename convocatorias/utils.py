import os
from django.utils import timezone
from .models import Modalidad

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

def obtener_becas(limite: int) -> list[Modalidad]:
    return Modalidad.objects.all()[:limite]

def obtener_disposicion(tamano_becas: int) -> str:
    return "" if tamano_becas >= 3 else "gdisp2" if tamano_becas == 2 else "gdisp1"
def procesar_becas() -> dict:
    diccionario_becas = {
        "becas": {
            "becas": (becas := obtener_becas(3)),
            "disposicion": obtener_disposicion(len(becas))
        }
    }
    return diccionario_becas
#----------------------------------
def numero_becas() -> list[Modalidad]:
    return Modalidad.objects.all().order_by()

def obtener_todas() -> dict:
    todas_becas = {
        "becas": {
            "becas": (becas := numero_becas()),
            "disposicion": obtener_disposicion(len(becas))
        }
    }
    return todas_becas