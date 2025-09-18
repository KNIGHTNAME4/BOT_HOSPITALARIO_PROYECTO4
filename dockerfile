
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

# Copiar el frontend
COPY public ./public

# Exponer puerto
EXPOSE 8080

# Servir el frontend
CMD ["serve", "-s", "public", "-l", "8080"]
