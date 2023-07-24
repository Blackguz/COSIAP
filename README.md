# Sistema de Apoyos COSIAP

El Sistema de Apoyos COSIAP es un proyecto desarrollado por el Laboratorio de Software Libre (LabSol), dirigido por Román Guzmán Valles, para el Consejo Zacatecano de Ciencia, Tecnología e Innovación (COZCyT). Este sistema permite la gestión de convocatorias, usuarios, administración y soporte de apoyos para los usuarios. Se ha diseñado y construido utilizando Django, un marco de trabajo de Python para el desarrollo de aplicaciones web.

## Colaboradores

- Román Guzmán Valles
- Adolfo Angel Garcia Luna
- Jorge Gael García Castorena
- Marco Antonio Pinedo Del Rio
- Leonardo Isaías Fernández Morales

## Requisitos

- Docker y Docker Compose.
- Python 3.9

## Instalación

1. Clona el repositorio a tu máquina local utilizando `git clone`.

```bash
git clone https://github.com/Blackguz/COSIAP.git
```

## Configuración de las variables de entorno

Crea un archivo .env en el directorio raíz del proyecto y añade las variables de entorno necesarias para la configuración de la aplicación. Se requieren las siguientes variables de entorno: HOST_BD, EMAIL_HOST, EMAIL_PASSWORD.

## Construcción y arranque del contenedor Docker
Con Docker y Docker Compose instalados, puedes construir y arrancar el contenedor utilizando docker-compose up.
```bash
docker-compose up
```
Una vez que los contenedores estén en marcha, podrás acceder a la aplicación en http://localhost:8000.

## Contribuciones

Las contribuciones son siempre bienvenidas. Para contribuir:

   - Haz un Fork del repositorio.
   - Crea una nueva rama con tus cambios (git checkout -b my-feature).
   - Haz commit de tus cambios (git commit -m 'Add some feature').
   - Haz push a la rama (git push origin my-feature).
   - Crea un nuevo Pull Request.

# Licencia

Este proyecto se distribuye bajo una licencia de uso libre, se pueden usar, copiar, estudiar, cambiar y distribuir el software y su código fuente. Se debe siempre dar crédito a los autores y no se puede utilizar con fines comerciales. Para más detalles, consulta el archivo LICENSE en este repositorio.