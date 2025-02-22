import json

def process_complex_json(file1, file2, output_file):
    try:
        # Leer los dos ficheros JSON
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)

        # Inicializar listas para almacenar tags y prompts
        all_tags_prompt = []
        all_tags_removed = []
        all_prompt = []

        # Procesar cada archivo JSON
        for data in (data1, data2):
            for key, value in data.items():
                # Añadir tags_prompt y tags_removed a las listas correspondientes
                all_tags_prompt.extend(value.get("tags_prompt", []))
                all_tags_removed.extend(value.get("tags_removed", []))
                # Añadir prompt a la lista de all_prompt (se asume que prompt es una cadena de texto)
                prompt = value.get("prompt", "")
                if prompt:
                    all_prompt.append(prompt)

        # Eliminar duplicados y ordenar alfabéticamente
        all_tags_prompt = sorted(set(all_tags_prompt))
        all_tags_removed = sorted(set(all_tags_removed))
        all_prompt = sorted(set(all_prompt))

        # Guardar el resultado en el fichero de salida
        with open(output_file, 'w') as out:
            json.dump({
                "all_tags_prompt": all_tags_prompt,
                "all_tags_removed": all_tags_removed,
                "all_prompt": all_prompt
            }, out, indent=4)
        
        print(f"Archivo procesado correctamente. Resultado guardado en {output_file}")
    except Exception as e:
        print(f"Error al procesar los archivos: {e}")

# Ejemplo de uso
file1 = ""
file2 = ""
output_file = "tags.json"

process_complex_json(file1, file2, output_file)
