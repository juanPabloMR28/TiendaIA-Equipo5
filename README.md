# TiendaIA-Equipo5

## Integrantes

A.- Juan Pablo Miranda Ramirez       25690164
B.- Ricardo Pinete Marinez           25690191
C.- Karla Teodaroa Galvan Acuña      25690704
C.- Abril Yamilet Turrubiates Paloma 25690660

## Despliegue en Render

Despliegue manual en Render:
- **Sitio estático:** https://tiendaia-web-equipo5-tjv6.onrender.com
- **Servicio IA:** https://tiendaia-ia-equipo5.onrender.com

Configuración manual:
- **Estático:** rama `main`, root `frontend`, build vacío, publish `.`
- **Servicio IA:** Python 3, rama `main`, root `ia_service`, build `pip install -r requirements.txt`, start `uvicorn app:app --host 0.0.0.0 --port $PORT`, plan `Free`
- **Variables:** `VENTAS_URL` (URL del gateway + `/api`), `MODELO_PATH=/tmp/modelo.joblib`, `PYTHON_VERSION=3.12.7`
