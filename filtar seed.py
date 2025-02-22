import os
import json
import re

# Ruta de la carpeta con las imágenes
ruta_carpeta = "IA V3/"

# Ruta del archivo JSON
ruta_json = "image_data_Pepe2.json"

def extraer_semilla(nombre_archivo):
    """Extrae la semilla del nombre del archivo."""
    match = re.search(r"-(\d+)\.(png|jpg)$", nombre_archivo)
    return match.group(1) if match else None

def cargar_datos_json(ruta_json):
    """Carga los datos desde un archivo JSON."""
    with open(ruta_json, "r") as file:
        return json.load(file)

def obtener_image_filename(datos_json, semilla):
    """Obtiene el image_filename para la semilla dada desde los datos del JSON."""
    for key, value in datos_json.items():
        if value.get("seed") == semilla:
            return value.get("image_filename")
    return None

def renombrar_imagenes():
    """Renombra las imágenes en la carpeta usando el JSON."""
    datos_json = cargar_datos_json(ruta_json)
    for archivo in os.listdir(ruta_carpeta):
        if archivo.endswith((".png", ".jpg")):  # Procesa archivos .png y .jpg
            semilla = extraer_semilla(archivo)
            if semilla:
                nuevo_nombre = obtener_image_filename(datos_json, semilla)
                if nuevo_nombre:
                    ruta_original = os.path.join(ruta_carpeta, archivo)
                    ruta_nueva = os.path.join(ruta_carpeta, os.path.basename(nuevo_nombre))
                    os.rename(ruta_original, ruta_nueva)
                    print(f"Renombrado: {archivo} -> {os.path.basename(nuevo_nombre)}")
                else:
                    print(f"No se encontró image_filename para la semilla {semilla}")
            else:
                print(f"No se pudo extraer semilla del archivo {archivo}")

# Ejecutar el script
renombrar_imagenes()
