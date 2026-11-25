import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import requests

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8081/api/productos"
TOTAL = int(sys.argv[2]) if len(sys.argv) > 2 else 150
HILOS = int(sys.argv[3]) if len(sys.argv) > 3 else 50
TIEMPO_ESPERA = 10

def pedir(_):
    try:
        return requests.get(URL, timeout=TIEMPO_ESPERA).status_code
    except requests.RequestException:
        return 0

if __name__ == "__main__":
    print(f"Ráfaga de {TOTAL} peticiones a {URL} con {HILOS} hilos...")
    inicio = time.perf_counter()
    with ThreadPoolExecutor(max_workers=HILOS) as grupo:
        codigos = list(grupo.map(pedir, range(TOTAL)))
    duracion = time.perf_counter() - inicio
    conteo = Counter(codigos)
    print(f"Duración: {duracion:.2f} s ({TOTAL / duracion:.1f} peticiones/s)")
    for codigo, veces in sorted(conteo.items()):
        nombre = {
            200: "OK",
            429: "Too Many Requests (límite)",
            0: "sin respuesta"
        }.get(codigo, "")
        print(f" {codigo:>3} {veces:>4} {nombre}")
    if conteo.get(429):
        print("El límite de peticiones está activo.")
    else:
        print("Ninguna petición recibió 429: revise limit_req en perimetro/nginx.conf.")