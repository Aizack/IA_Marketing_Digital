# Dockerfile - Marketing AI Studio Engine (Antigravity v2.0 Microservice)
FROM python:3.11-slim

# Metadatos
LABEL maintainer="Antigravity Marketing AI Studio"
LABEL description="Microservicio de Agencia de Marketing Digital con Agentes Nivel 1 y Nivel 2"

# Instalar dependencias básicas del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar e instalar requerimientos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del microservicio
COPY engine.py server.py ./
COPY gui/ ./gui/

# Variables de entorno por defecto
ENV PORT=8090 \
    PYTHONUNBUFFERED=1 \
    AGENT_ENV=production

EXPOSE 8090

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8090/health || exit 1

CMD ["python", "server.py"]
