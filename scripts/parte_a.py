import time
import requests

def medir_peticion(nombre, metodo, url, **kwargs):
    t0 = time.perf_counter()
    try:
        r = requests.request(metodo, url, timeout=10, **kwargs)
        ms = (time.perf_counter() - t0) * 1000
        print(f"=== {nombre} ===")
        print(f"Método: {metodo} | Código: {r.status_code} | Tiempo: {ms:.1f} ms | Tamaño: {len(r.content)} bytes")
        if r.status_code == 200:
            print("Respuesta (fragmento):", str(r.json())[:150])
        else:
            print("Respuesta texto:", r.text[:100])
        print()
    except Exception as e:
        print(f"Error en {nombre}: {e}\n")

# 1. Geocodificación
medir_peticion("1. Geocodificación Ciudad Valles", "GET", 
               "https://geocoding-api.open-meteo.com/v1/search", 
               params={"name": "Ciudad Valles", "count": 1, "language": "es"})

# 2. Clima actual
medir_peticion("2. Clima Ciudad Valles", "GET", 
               "https://api.open-meteo.com/v1/forecast", 
               params={"latitude": 21.98, "longitude": -99.01, "current": "temperature_2m"})

# 3. POST de prueba
medir_peticion("3. POST en JSONPlaceholder", "POST", 
               "https://jsonplaceholder.typicode.com/posts", 
               json={"title": "hola", "body": "desde script", "userId": 1})

# 4. Recurso inexistente (404)
medir_peticion("4. Recurso Inexistente", "GET", 
               "https://pokeapi.co/api/v2/pokemon/no-existe")
