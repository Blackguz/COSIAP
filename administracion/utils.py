from convocatorias.models import Solicitud
from django.db.models import Count
from django.contrib.auth.decorators import user_passes_test

# Obtenemos el número de solicitudes por nivel de estudios
def get_solicitudes_por_nivel():
    niveles_estudios = ["Licenciatura", "Maestría", "Doctorado"]
    solicitudes_por_nivel = []

    for nivel in niveles_estudios:
        solicitudes = Solicitud.objects.filter(id_solicitante__ultimo_grado_estudios=nivel)
        solicitudes_por_nivel.append(solicitudes.count())

    return niveles_estudios, solicitudes_por_nivel

# Obtenemos el número de solicitudes por género
def get_generos_solicitantes():
    generos_solicitantes = Solicitud.objects.values('id_solicitante__genero').annotate(total=Count('id_solicitante__genero'))
    generos = {
        'Masculino': 0,
        'Femenino': 0
    }
    for genero in generos_solicitantes:
        if genero['id_solicitante__genero'] == 'M':
            generos['Masculino'] += genero['total']
        elif genero['id_solicitante__genero'] == 'F':
            generos['Femenino'] += genero['total']
    return generos
