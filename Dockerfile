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

# Copia el script de entrada
COPY ./entrypoint.sh /app/entrypoint.sh

# Comando de entrada
ENTRYPOINT ["/app/entrypoint.sh"]

# Copiar el proyecto
COPY . .
