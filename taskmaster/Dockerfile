# Utiliza una imagen base de Python
FROM python:3.10-slim-bullseye

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al directorio de trabajo
COPY . /app

# Instalar las dependencias del proyecto y realizar las migraciones
RUN pip install -r requirements.txt && python manage.py migrate

# Expone el puerto 8000 para que sea accesible desde el host
EXPOSE 8000

# Ejecuta el comando para iniciar el servidor de desarrollo
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
