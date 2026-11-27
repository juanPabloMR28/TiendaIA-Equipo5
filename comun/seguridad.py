"""Verificación de API Keys entre servicios (Laboratorio 6).

Este módulo se copia en cada microservicio protegido (clientes, productos, ...).
Antes de atender una petición pregunta al Auth-Service si la API Key recibida en la
cabecera x-api-key es válida, y guarda la respuesta 60 s en memoria (caché).

Uso en un servicio:
    from seguridad import requiere_servicio
    app = FastAPI(..., dependencies=[Depends(requiere_servicio)])
"""
import os
import time

import requests  # cliente HTTP para consultar al Auth-Service
from fastapi import Header, HTTPException, Request

# ---------------------------------------------------------------- Configuración
# En Docker Compose el Auth-Service se llama por su nombre de servicio ("auth").
AUTH_URL = os.getenv("AUTH_URL", "http://auth:8000")
TIEMPO_ESPERA = 3  # segundos: si Auth no responde, no se bloquea el servicio

# Caché en memoria: clave -> (servicio, momento en que expira). Evita llamar a Auth
# en CADA petición, lo que añadiría latencia y lo volvería un cuello de botella.
_cache: dict[str, tuple[str, float]] = {}

# Tiempo de vida de la caché. Compromiso: una clave revocada puede seguir sirviendo
# hasta 60 s en el servicio que ya la tenía guardada.
TTL = 60

# Sesión de requests: reutiliza la conexión TCP con Auth entre validaciones.
sesion = requests.Session()


def requiere_servicio(request: Request, x_api_key: str | None = Header(default=None)):
    """Dependencia global de FastAPI: exige una API Key válida en x-api-key.

    Devuelve el nombre del servicio que llama (o None en /health). Responde 401 si
    no se envió clave y 403 si Auth la rechaza.
    """
    if request.url.path == "/health":  # el health check queda abierto (lo usa Docker)
        return None
    if not x_api_key:
        raise HTTPException(401, "API Key requerida en x-api-key")