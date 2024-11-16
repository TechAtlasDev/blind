# Usa una imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia todos los archivos de tu proyecto a /app en el contenedor
COPY . .

# Activa el entorno virtual
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Instala las dependencias
RUN pip install -r requirements.txt

# Define el comando de inicio del bot
CMD ["python3", "manager.py"]
