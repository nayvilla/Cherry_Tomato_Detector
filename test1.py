from controllers.detection_controller import process_and_save_image, project_root

# Define la ruta de la imagen de prueba
image_path = project_root / "src/capture_images/Tomate-cherry.png"  # Cambia el nombre si tienes otra imagen

# Llama a la función para procesar la imagen
adjusted_probs = process_and_save_image(image_path)

# Muestra las probabilidades ajustadas
print("Probabilidades ajustadas:", adjusted_probs)

