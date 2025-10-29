# Dockerfile
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo
WORKDIR /app

# Copiamos los requirements.txt y los instalamos
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del proyecto
COPY . .

# Exponemos el puerto 8000
EXPOSE 8000

# Comando para correr la app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]