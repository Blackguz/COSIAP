import os
from django.utils import timezone
from .models import Modalidad, AtributosFormulario, Formulario

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
    modalidades = Modalidad.objects.all()[:limite]
    resultado = {}
    becas = []

    for modalidad in modalidades:
        resultado["beca"]=modalidad
        resultado["requisitos"]=obtener_requisitos(modalidad)
        becas.append(resultado)
        resultado = {}
    return becas

def obtener_disposicion(tamano_becas: int) -> str:
    return "" if tamano_becas >= 3 else "gdisp2" if tamano_becas == 2 else "gdisp1"

def obtener_requisitos(modalidad: Modalidad) -> list[AtributosFormulario]:
    formulario = Formulario.objects.filter(id_modalidad=modalidad)
    atributos = AtributosFormulario.objects.filter(id_formulario=formulario[0])
    return [*atributos]


def procesar_becas() -> dict:
    diccionario_becas = {
        "becas": (becas := obtener_becas(3)),
        "disposicion": obtener_disposicion(len(becas)),
    }
    return diccionario_becas