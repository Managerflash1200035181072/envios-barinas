# Imagen base de Python para el backend Django
FROM python:3.11-slim

# Evitar la creación de archivos .pyc y permitir logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar las dependencias del proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente del backend
COPY . .

# Puerto interno del servidor de desarrollo de Django
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
