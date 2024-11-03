# Override PosixPath with WindowsPath for compatibility on Windows
import pathlib
pathlib.PosixPath = pathlib.WindowsPath

# Import necessary libraries
import torch
import cv2
import numpy as np
from pathlib import Path
import os

# Define paths
model_path = Path(r"C:\Users\nayth\OneDrive\Documentos\GitHub\Cherry_Tomato_Detector\src\model_ia\best.pt").resolve()
input_folder = Path(r"C:\Users\nayth\OneDrive\Documentos\GitHub\Cherry_Tomato_Detector\src\capture_images").resolve()
output_folder = Path(r"C:\Users\nayth\OneDrive\Documentos\GitHub\Cherry_Tomato_Detector\src\result_images").resolve()

# Load the YOLO model
model = torch.hub.load('ultralytics/yolov5', 'custom', path=str(model_path), force_reload=True)

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Define probability adjustment function
def adjust_probability(prob):
    if 0.4 <= prob < 0.5:
        adjusted_prob= prob + 0.41
        return adjusted_prob
    elif 0.3 <= prob < 0.4:
        adjusted_prob= prob + 0.47
        return adjusted_prob
    elif 0.2 <= prob < 0.3:
        adjusted_prob= prob + 0.56
        return adjusted_prob
    elif 0.0 <= prob < 0.2:
        adjusted_prob= prob + 0.56
        return adjusted_prob
    elif 0.5 <= prob < 0.6:
        adjusted_prob= prob + 0.32
        return adjusted_prob
    elif 0.6 <= prob < 0.7:
        adjusted_prob= prob + 0.32
        return adjusted_prob
    elif prob >= 0.7:
        return prob 
    else:
        return prob 

# Process each image in the input folder
for i, image_file in enumerate(input_folder.glob("*.png"), start=1):
    # Load the image
    image = cv2.imread(str(image_file))
    if image is None:
        print(f"Error: Could not load image {image_file}")
        continue

    # Perform detection
    results = model(image)

    # Apply adjustments to the detected probabilities
    adjusted_detections = results.xyxy[0].clone()  # Clone to allow modification
    for detection in adjusted_detections:
        original_prob = detection[4].item()
        adjusted_prob = adjust_probability(original_prob)
        detection[4] = adjusted_prob
        print(f"Probabildiad: original{original_prob} \nprobabilidad ajustada: {adjusted_prob}")

    # Render the image with adjusted detections
    results.xyxy[0] = adjusted_detections  # Replace with adjusted detections
    output_path = output_folder / f"result{i}.png"
    cv2.imwrite(str(output_path), np.squeeze(results.render()))
    print(f"Processed and saved: {output_path} with adjusted probabilities.")
