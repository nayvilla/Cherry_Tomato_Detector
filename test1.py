#from controllers.detection_controller import process_and_save_image, project_root

# Define la ruta de la imagen de prueba
#image_path = project_root / "src/capture_images/Tomate-cherry.png"  # Cambia el nombre si tienes otra imagen

# Llama a la función para procesar la imagen
#adjusted_probs = process_and_save_image(image_path)

# Muestra las probabilidades ajustadas
#print("Probabilidades ajustadas:", adjusted_probs)


import serial
import time

def test_arduino_connection(port):
    try:
        # Establecer la conexión serial
        ser = serial.Serial(port, 9600, timeout=2)
        
        # Esperar un momento para estabilizar la conexión
        time.sleep(2)
        
        # Vaciar el buffer de entrada para limpiar datos antiguos
        ser.reset_input_buffer()
        
        # Enviar el comando CONNECT
        ser.write(b'CONNECT\n')
        
        # Esperar brevemente para darle tiempo al Arduino para responder
        time.sleep(2)
        
        # Leer la respuesta en un bucle para asegurarse de obtener todos los datos
        response = ""
        start_time = time.time()
        while (time.time() - start_time) < 3:  # Espera hasta 3 segundos
            if ser.in_waiting > 0:
                response += ser.readline().decode().strip()
                if "Conectado" in response:
                    break
        
        # Imprimir la respuesta para verificar si es correcta
        print(f"Respuesta del Arduino: {response}")
        
        # Cerrar la conexión serial
        ser.close()
        
        # Verificar si la respuesta contiene "Conectado"
        return "Conectado" in response

    except Exception as e:
        print(f"Error de conexión: {e}")
        return False

import os

# Ruta actual del archivo
current_path = os.path.abspath(__file__)
root_path = os.path.dirname(os.path.dirname(current_path))
capture_path = os.path.join(root_path, "Cherry_Tomato_Detector", "src", "capture_images")

# Imprimir la ruta raíz y la ruta de captura
print("Ruta raíz del proyecto:", root_path)
print("Ruta de captura de imágenes:", capture_path)




# Cambia 'COM3' por el puerto adecuado para tu Arduino
#if __name__ == "__main__":
#    port = 'COM4'  # Cambia esto al puerto correcto
#    if test_arduino_connection(port):
#        print("Conexión exitosa con el Arduino.")
#    else:
#        print("No se recibió la respuesta esperada del Arduino.")
