import pathlib

import torch
from controllers.detection_controller import process_and_save_image, project_root

# Define la ruta de la imagen de prueba
image_path = project_root / "src/capture_images/captureImage1.png"  # Cambia el nombre si tienes otra imagen
# Configuración para compatibilidad con Windows
pathlib.PosixPath = pathlib.WindowsPath

# Determina automáticamente la ruta raíz del proyecto
model_path = project_root / "src/model_ia/detect_tomato_best.pt"

# Cargar el modelo YOLO
model = torch.hub.load('ultralytics/yolov5', 'custom', path=str(model_path), force_reload=True)
# Llama a la función para procesar la imagen
adjusted_probs = process_and_save_image(image_path, model)

# Muestra las probabilidades ajustadas
print("Probabilidades ajustadas:", adjusted_probs)

