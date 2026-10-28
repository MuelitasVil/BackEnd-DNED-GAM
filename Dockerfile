# Construir desde la raiz del repositorio: docker build -t gam-backend:1.0 .
# Estructura esperada: app/main.py y app/requirements.txt.
# main.py debe exportar la instancia FastAPI como `app`.
ARG PYTHON_IMAGE=python:3.11-slim-bookworm

FROM ${PYTHON_IMAGE} AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1

ARG GAM_VERSION=7.49.0
ARG MSAL_VERSION=1.39.0

# Compiladores solo en la etapa de construccion. Las librerias MySQL permiten
# compilar mysqlclient si el requirements.txt real lo utiliza.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential pkg-config default-libmysqlclient-dev ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/api-venv \
    && python -m venv /opt/gam-venv

WORKDIR /build
COPY app/requirements.txt ./requirements.txt

# MSAL obtiene tokens de Entra ID; httpx realiza las solicitudes a Graph.
# httpx debe estar en requirements.txt, como en el README suministrado.
RUN /opt/api-venv/bin/python -m pip install \
        -r requirements.txt "msal==${MSAL_VERSION}" \
    && /opt/api-venv/bin/python -m pip check \
    && /opt/api-venv/bin/python -c "import fastapi, uvicorn, httpx, msal"

# GAM queda aislado de las dependencias de la API, pero su CLI esta disponible.
RUN /opt/gam-venv/bin/python -m pip install "gam7==${GAM_VERSION}" \
    && /opt/gam-venv/bin/python -m pip check \
    && test -x /opt/gam-venv/bin/gam

FROM ${PYTHON_IMAGE} AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/opt/api-venv/bin:${PATH}" \
    HOME=/home/appuser \
    GAMCFGDIR=/var/lib/gam/config \
    GAM_WORKDIR=/var/lib/gam/work \
    GAM_EXECUTABLE=/opt/gam-venv/bin/gam

# libmariadb3 es la biblioteca cliente; no instala el servidor MySQL.
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates libmariadb3 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid 10001 --create-home appuser \
    && mkdir -p /var/lib/gam/config /var/lib/gam/work \
    && chown -R appuser:appuser /var/lib/gam

COPY --from=builder /opt/api-venv /opt/api-venv
COPY --from=builder /opt/gam-venv /opt/gam-venv

RUN ln -s /opt/gam-venv/bin/gam /usr/local/bin/gam

WORKDIR /app
# Crear .dockerignore antes de construir para excluir secretos y entornos locales.
COPY app/ ./

RUN mkdir -p /app/logs \
    && chown -R appuser:appuser /app/logs

USER appuser
EXPOSE 8000

# La autorizacion de GAM se realiza en ejecucion usando un volumen persistente.
# No ejecutar `gam create project` ni `gam oauth create` durante el build.
CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]
