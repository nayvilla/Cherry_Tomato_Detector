import sys
import numpy as np
from pathlib import Path

# Añadir el directorio `yolov5` al path
project_root = Path(__file__).resolve().parent / 'yolov5'
sys.path.append(str(project_root))

import pathlib
pathlib.PosixPath = pathlib.WindowsPath

import torch
import cv2
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.general import non_max_suppression, scale_boxes
from yolov5.utils.torch_utils import select_device

def detect_tomato(image_path, model_path, output_path, img_size=416, conf_threshold=0.1, iou_threshold=0.45, device_type='cpu'):
    # Convertir `output_path` a Path si aún no lo es
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)  # Crear la carpeta si no existe

    # Configuración del dispositivo y carga del modelo
    device = select_device(device_type)
    model = DetectMultiBackend(model_path, device=device)
    model.warmup(imgsz=(1, 3, img_size, img_size))  # Calentamiento del modelo

    # Leer la imagen y preprocesarla
    image = cv2.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen en la ruta: {image_path}")
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_tensor = torch.from_numpy(image_rgb).permute(2, 0, 1).float().to(device) / 255.0
    img_tensor = img_tensor.unsqueeze(0)

    # Detección
    with torch.no_grad():
        pred = model(img_tensor)

    # Aplicar Non-Maximum Suppression (NMS)
    pred = non_max_suppression(pred, conf_threshold, iou_threshold, classes=None, agnostic=False)

    # Mapeo de clases (modifica según las clases de tu modelo)
    class_names = {0: "Maduro", 1: "Premaduro", 2: "Inmaduro", 3: "Malo"}

    # Variables para almacenar el mejor resultado
    best_result = None
    best_confidence = 0
    render_image = image.copy()  # Crear una copia de la imagen para renderizar los resultados

    # Procesar detecciones
    for i, det in enumerate(pred):
        if det is not None and len(det):
            # Escalar las coordenadas a la imagen original
            det[:, :4] = scale_boxes(img_tensor.shape[2:], det[:, :4], image.shape).round()
            for *xyxy, conf, cls in det:
                # Obtener el nombre de la clase y la confianza
                confidence_val = conf.item()
                confidence = f"{confidence_val * 100:.2f}%"
                class_name = class_names.get(int(cls), "desconocido")

                # Actualizar el mejor resultado si esta confianza es mayor
                if confidence_val > best_confidence:
                    best_confidence = confidence_val
                    best_result = f"Estado: {class_name} con {confidence}"
                    print(f"Nuevo mejor resultado: {best_result}")

                # Dibujar rectángulo y etiqueta en la imagen
                label = f"{class_name} {confidence}"
                x1, y1, x2, y2 = map(int, xyxy)  # Convertir coordenadas a enteros
                cv2.rectangle(render_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(render_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Guardar la imagen con los resultados renderizados en `output_path`
    cv2.imwrite(str(output_path), render_image)
    print(f"Imagen procesada y guardada en: {output_path}")

    return best_result
