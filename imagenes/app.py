"""Microservicio Imágenes de TiendaIA (Laboratorio 4).

Guarda las fotos de los productos en un almacenamiento de objetos con API S3
(SeaweedFS en el laboratorio) y entrega URL prefirmadas para descargarlas.
Consulta y actualiza al microservicio Productos por HTTP con requests; la
lógica de S3 vive en almacen.py.
"""
import hashlib # huella SHA-256 para verificar la integridad del archivo
import os
import uuid # nombres únicos: dos fotos nunca se sobrescriben entre sí

import requests # cliente HTTP para llamar al microservicio Productos
from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from almacen import AlmacenS3 # adaptador S3 (subir, url, eliminar)

# ---------------------------------------------------------------- Configuración
PRODUCTOS_URL = os.getenv("PRODUCTOS_URL", "http://productos:8000")
# Tipos MIME aceptados -> extensión del archivo que se guarda en el bucket
TIPOS = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}
MAX_BYTES = 5 * 1024 * 1024 # 5 MB: límite para no llenar el almacenamiento
almacen = AlmacenS3() # al arrancar se conecta a S3 y revisa el bucket
TIEMPO_ESPERA = 5 # segundos máximos de espera a Productos
sesion = requests.Session() # reutiliza conexiones TCP con Productos
app = FastAPI(title="TiendaIA - Imágenes")

# ---------------------------------------------------------------- Subir imagen
@app.post("/imagenes", status_code=201)
async def subir(producto_id: int = Form(gt=0), archivo: UploadFile = File(...)):
    """Recibe un formulario multipart (producto_id + archivo) y guarda la imagen.

    Responde 201 con la clave del objeto; 404 si el producto no existe, 415 si
    el tipo no es imagen permitida, 413 si pasa de 5 MB y 422 si producto_id
    no es un entero mayor que cero (Form(gt=0) lo valida FastAPI).
    """

    p = producto(producto_id) # 404 aquí si el producto no existe
    if archivo.content_type not in TIPOS: # 415 = tipo de contenido no soportado
        raise HTTPException(415, "Solo se aceptan JPEG, PNG o WebP")
    datos = await archivo.read() # bytes completos del archivo subido
    if len(datos) > MAX_BYTES: # 413 = la carga es demasiado grande
        raise HTTPException(413, "La imagen excede 5 MB")
    # Clave = "ruta" del objeto dentro del bucket. S3 no tiene carpetas reales:
    # el prefijo productos/<id>/ solo agrupa las claves de cada producto.
    clave = f"productos/{producto_id}/{uuid.uuid4().hex}.{TIPOS[archivo.content_type]}"
    sha = hashlib.sha256(datos).hexdigest() # huella para comprobar integridad
    # Los metadatos viajan junto al objeto en S3 (cabeceras x-amz-meta-*)
    almacen.subir(clave, datos, archivo.content_type, {"sha256": sha})
    if p.get("imagen_key"): # reemplazo: borrar la anterior
        almacen.eliminar(p["imagen_key"])
    asociar(producto_id, clave) # Productos guarda solo la clave
    return {"producto_id": producto_id, "clave": clave,
            "bytes": len(datos), "sha256": sha}