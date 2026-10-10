"""Mide la latencia de un endpoint desplegado en la nube (Laboratorio 1)."""
import statistics as st
import sys
import time
import requests

if len(sys.argv) < 2:
    print("Uso: python scripts/medir_latencia.py <URL_ENDPOINT> [NUM_PETICIONES]")
    sys.exit(1)

URL = sys.argv[1]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 30
TIEMPO_ESPERA = 60

with requests.Session() as sesion:
    # Primera petición (Arranque en frío)[cite: 31]
    t0 = time.perf_counter()
    r = sesion.get(URL, timeout=TIEMPO_ESPERA)
    primera = (time.perf_counter() - t0) * 1000

    tiempos, errores = [], 0
    for _ in range(N):
        t0 = time.perf_counter()
        res = sesion.get(URL, timeout=TIEMPO_ESPERA)
        errores += res.status_code >= 400
        tiempos.append((time.perf_counter() - t0) * 1000)

    tiempos.sort()
    print(f"URL: {URL}")
    print(f"Primera petición: {primera:.0f} ms (código {r.status_code})")
    print(f"Siguientes ({N}): p50={st.median(tiempos):.0f} ms | "
          f"p95={tiempos[int(0.95 * N) - 1]:.0f} ms | "
          f"máx={tiempos[-1]:.0f} ms | errores={errores}")
