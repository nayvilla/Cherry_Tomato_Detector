import sys
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

def detect_tomato(image_path, model_path, img_size=416, conf_threshold=0.1, iou_threshold=0.45, device_type='cpu'):
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
    class_names = {0: "Maduro", 1: "Premaduro", 2: "Inmaduro", 3: "Dañado"}

    # Lista para almacenar los resultados en el formato especificado
    results = []

    # Procesar detecciones
    for det in pred:
        if det is not None and len(det):
            # Escalar las coordenadas a la imagen original
            det[:, :4] = scale_boxes(img_tensor.shape[2:], det[:, :4], image.shape).round()
            for *xyxy, conf, cls in det:
                # Obtener el nombre de la clase y la confianza
                confidence = f"{conf.item() * 100:.2f}%"
                class_name = class_names.get(int(cls), "desconocido")

                # Agregar resultado en el formato especificado
                results.append(f"Estado: {class_name} con {confidence}")

    return results


# Ejemplo de uso de la función
image_path = r"C:\Users\nayth\OneDrive\Documentos\GitHub\Cherry_Tomato_Detector\src\capture_images\captureImage1.png"
model_path = r"C:\Users\nayth\OneDrive\Documentos\GitHub\Cherry_Tomato_Detector\src\model_ia\best.pt"
detections = detect_tomato(image_path, model_path)

# Imprimir los resultados
print(f'Este es fuea del for: {detections}')
for detection in detections:
    print(detection)
