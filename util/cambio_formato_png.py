import os
from PIL import Image

# Definir rutas de entrada y salida
input_folder = r"C:\Users\nayth\Downloads\image\image"
output_folder = r"C:\Users\nayth\Downloads\image\imagenpng"

# Crear la carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Recorrer todos los archivos en la carpeta de entrada
for filename in os.listdir(input_folder):
    # Construir la ruta completa de cada archivo
    file_path = os.path.join(input_folder, filename)

    # Verificar si el archivo es una imagen soportada (ignorar directorios o archivos no soportados)
    if filename.lower().endswith(('.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp', '.avif', '.jfif')):
        try:
            # Abrir la imagen
            with Image.open(file_path) as img:
                # Convertir a formato PNG y guardar en la carpeta de salida
                output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.png")
                img.save(output_path, "PNG")
                print(f"Imagen convertida y guardada en: {output_path}")
        except Exception as e:
            print(f"Error al convertir {filename}: {e}")
    else:
        print(f"{filename} no es un formato soportado y se ha omitido.")

print("Conversión de imágenes completada.")
