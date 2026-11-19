import random
import statistics
import sys
import threading
import time
import requests

URL = sys.argv[1] if len(sys.argv) > 1 else "http://ia:8000"
DURACION = int(sys.argv[2]) if len(sys.argv) > 2 else 180
HILOS = int(sys.argv[3]) if len(sys.argv) > 3 else 8
INTERVALO = 15
TIEMPO_ESPERA = 10
latencias = []
errores = 0
candado = threading.Lock()
fin = time.time() + DURACION

def trabajador():
    global errores
    sesion = requests.Session()
    while time.time() < fin:
        params = {
            "producto_id": random.randint(1, 5),
            "mes": random.randint(1, 12),
            "precio": random.choice([35, 60, 90, 120, 150])
        }
        inicio = time.perf_counter()
        try:
            r = sesion.get(f"{URL}/ia/predict", params=params, timeout=TIEMPO_ESPERA)
            ok = r.status_code == 200
        except requests.RequestException:
            ok = False
        ms = (time.perf_counter() - inicio) * 1000
        with candado:
            if ok:
                latencias.append(ms)
            else:
                errores += 1

if __name__ == "__main__":
    print(f"Carga contra {URL}: {HILOS} hilos durante {DURACION} s", flush=True)
    hilos = [threading.Thread(target=trabajador, daemon=True) for _ in range(HILOS)]
    for h in hilos:
        h.start()
    t0 = anterior = time.time()
    print(" t(s) peticiones errores peticiones/s media(ms) p95(ms)", flush=True)
    while time.time() < fin:
        time.sleep(min(INTERVALO, fin - time.time() + 0.5))
        ahora = time.time()
        segundos, anterior = ahora - anterior, ahora
        with candado:
            datos, fallas = sorted(latencias), errores
            latencias.clear()
            errores = 0
        if datos:
            media = statistics.mean(datos)
            p95 = datos[int(0.95 * len(datos)) - 1] if len(datos) > 1 else datos[0]
        else:
            media = p95 = 0.0
        print(
            f"{ahora - t0:6.0f} {len(datos):10d} {fallas:7d} "
            f"{len(datos) / segundos:12.1f} {media:9.1f} {p95:7.1f}",
            flush=True
        )
    for h in hilos:
        h.join(timeout=TIEMPO_ESPERA)
    print("Carga terminada. Observe cómo el HPA reduce las réplicas en unos minutos.")