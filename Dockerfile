# Imagen base oficial ligera de Python 3.12
FROM python:3.12-slim

# Evita que Python escriba archivos .pyc y que bufere la salida de logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=analizador.settings

WORKDIR /app

# Instalar dependencias primero para aprovechar el cache de capas de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . .

# Puerto en el que escucha el servidor de desarrollo de Django
EXPOSE 8000

# Ejecutar la aplicación expuesta en todas las interfaces del contenedor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
