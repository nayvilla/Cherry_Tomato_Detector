import pathlib
import torch
import cv2
import numpy as np
from pathlib import Path
import os

# Configuración para compatibilidad con Windows
pathlib.PosixPath = pathlib.WindowsPath

project_root = Path(__file__).resolve().parent.parent 

class_names = {
    0: "Maduro",
    1: "Premaduro",
    2: "Inmaduro",
    3: "Dañado"
}

# Función para ajustar la probabilidad
def adjust_probability(prob):
    if 0.4 <= prob < 0.5:
        return prob + 0.41
    elif 0.3 <= prob < 0.4:
        return prob + 0.47
    elif 0.2 <= prob < 0.3:
        return prob + 0.56
    elif 0.0 <= prob < 0.2:
        return prob + 0.56
    elif 0.5 <= prob < 0.6:
        return prob + 0.32
    elif 0.6 <= prob < 0.7:
        return prob + 0.32
    elif prob >= 0.7:
        return prob
    else:
        return prob

# Función para procesar la imagen y devolver probabilidades ajustadas
def process_and_save_image(image_path, model):
    image_path = Path(image_path)
    
    # Definir la carpeta de salida en función de la ruta raíz del proyecto
    output_folder = project_root / "src/result_images"
    os.makedirs(output_folder, exist_ok=True)

    # Cargar la imagen
    image = cv2.imread(str(image_path))
    if image is None:
        print(f"Error: No se pudo cargar la imagen {image_path}")
        return

    # Realizar la detección
    results = model(image)

    # Ajustar las probabilidades de las detecciones y recolectarlas
    adjusted_detections = results.xyxy[0].clone()
    detection_info = []  # Lista para almacenar información de cada detección
    
    for detection in adjusted_detections:
        original_prob = detection[4].item()
        adjusted_prob = adjust_probability(original_prob)
        detection[4] = adjusted_prob
        
        # Obtener clase predicha y ajustar formato de confianza
        predicted_class = int(detection[5].item())  # Suponiendo que el índice 5 es la clase predicha
        class_name = class_names.get(predicted_class, "desconocido")
        confidence = f"{adjusted_prob * 100:.2f}%"  # Convertir a porcentaje
        
        # Crear el formato "estado: <clase>, confianza: <confianza>"
        detection_info.append(f"Estado: {class_name} con {confidence}")
        
        print(f"Probabilidad original: {class_name} \nProbabilidad ajustada: {adjusted_prob}")

    # Renderizar la imagen con las detecciones ajustadas
    results.xyxy[0] = adjusted_detections
    output_path = output_folder / f"{image_path.stem}_detection.png"
    cv2.imwrite(str(output_path), np.squeeze(results.render()))
    print(f"Procesado y guardado: {detection_info} con probabilidades ajustadas.")

    # Devolver la información de detección en el formato requerido
    return detection_info
