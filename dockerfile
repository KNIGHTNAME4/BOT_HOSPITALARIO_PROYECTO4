# Imagen base con Python ya lista
FROM python:3.13.7-slim-bookworm

# Instalar Node.js y Git
RUN apt-get update && apt-get install -y \
    curl git \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Definir carpeta de trabajo
WORKDIR /app

# Exponer puertos (ejemplo: backend en 8000, frontend en 4200)
EXPOSE 8000 4200

# Comando por defecto (abre bash para trabajar en el contenedor)
CMD ["/bin/bash"]
