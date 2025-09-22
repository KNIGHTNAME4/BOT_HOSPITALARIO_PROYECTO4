# Imagen base con Python + Node
FROM python:3.13.7-slim-bookworm

# Instalar Node.js y Git
RUN apt-get update && apt-get install -y \
    curl git \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g serve \
    && rm -rf /var/lib/apt/lists/*

# Carpeta de trabajo
WORKDIR /app

# Copiar toda la aplicación
COPY app_software/ ./app_software

# Instalar dependencias Python
WORKDIR /app/app_software
RUN pip install --no-cache-dir -r requirements.txt

# Exponer puerto
EXPOSE 5000

# Ejecutar Flask con Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
