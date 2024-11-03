import pathlib
import torch
import cv2
import numpy as np
from pathlib import Path
import os

# Configuración para compatibilidad con Windows
pathlib.PosixPath = pathlib.WindowsPath

# Determina automáticamente la ruta raíz del proyecto
project_root = Path(__file__).resolve().parent.parent 
model_path = project_root / "src/model_ia/best.pt"

# Cargar el modelo YOLO
model = torch.hub.load('ultralytics/yolov5', 'custom', path=str(model_path), force_reload=True)

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
def process_and_save_image(image_path):
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
    adjusted_probabilities = []
    for detection in adjusted_detections:
        original_prob = detection[4].item()
        adjusted_prob = adjust_probability(original_prob)
        detection[4] = adjusted_prob
        adjusted_probabilities.append(adjusted_prob)
        print(f"Probabilidad original: {original_prob} \nProbabilidad ajustada: {adjusted_prob}")

    # Renderizar la imagen con las detecciones ajustadas
    results.xyxy[0] = adjusted_detections
    output_path = output_folder / f"{image_path.stem}_detection.png"
    cv2.imwrite(str(output_path), np.squeeze(results.render()))
    print(f"Procesado y guardado: {output_path} con probabilidades ajustadas.")

    # Devolver las probabilidades ajustadas
    return adjusted_probabilities
