# Imagen base de Python
FROM python:3.9

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN python manage.py loaddata convocatorias/fixtures/estatus_initial_data
# Copiar el proyecto
COPY . .
