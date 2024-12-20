# controller.py
import glob
import os
import pathlib
import time
from typing import Counter
import flet as ft
import cv2
import base64
import threading

import torch

from views.bienvenida_view import BienvenidaView
from views.detector_view import DetectorView
from model.arduino_model import ArduinoModel
from model.camera_model import CameraModel
from controllers.detection_controller import detect_tomato, project_root


class MainController:
    def __init__(self, page):
        self.page = page
        self.arduino = ArduinoModel()
        self.camera = CameraModel()
        self.bienvenida_view = BienvenidaView(page, self)
        self.detector_view = DetectorView(page, self)
        self.update_camera_list()
        self.cap = None  
        self.camera_feed_active = False
        current_path = os.path.abspath(__file__)
        root_path = os.path.dirname(os.path.dirname(current_path))
        self.model = os.path.join(root_path, "src", "model_ia", "best.pt")
        #self.model = project_root / "src/model_ia/best.pt"

    def show_bienvenida(self):
        self.page.window_width = 750
        self.page.window_height = 700 
        self.page.views.clear()
        self.page.views.append(self.bienvenida_view.build())
        self.page.update()

    def show_detector(self):
        self.page.window_width = 1000
        self.page.window_height = self.page.window_height * 1.2
        self.page.views.clear()
        self.page.views.append(self.detector_view.build())
        self.page.update()

    def conectar_arduino(self):
        selected_port = self.detector_view.dropdown_ports.value
        if not selected_port:
            self.detector_view.set_status("Error al conectar")
            self.detector_view.display_console_output("No se seleccionó un puerto para conectar.")
            return
        connection_result = self.arduino.connect(selected_port)
        print(f"Resultado de la conexión al Arduino: {connection_result}")
        if connection_result:
            self.detector_view.set_status("Conectado")
            self.detector_view.display_console_output("Arduino conectado")
        else:
            self.detector_view.set_status("Error al conectar")
            self.detector_view.display_console_output("Error al conectar al Arduino")
            
    def handle_conectar_arduino(self):
        self.detector_view.show_loading(True)
        threading.Thread(target=self.conectar_arduino_thread).start()

    def conectar_arduino_thread(self):
        try:
            self.conectar_arduino()
        finally:
            self.detector_view.show_loading(False)

    def update_camera_list(self):
        cameras = self.camera.get_cameras()
        self.detector_view.dropdown_cameras.options = [
            ft.dropdown.Option(str(index)) for index, _ in enumerate(cameras)
        ]
        self.page.update()

    def start_camera_feed(self):
        # Check if a camera is already active to prevent multiple threads
        if self.camera_feed_active:
            print("Camera feed is already active.")
            return

        selected_camera_index = self.detector_view.dropdown_cameras.value
        if selected_camera_index is None:
            print("No camera selected.")
            self.detector_view.display_console_output("Seleccione una cámara para iniciar.")
            return

        camera_index = int(selected_camera_index.split()[-1])
        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_MSMF if camera_index == 0 else cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            print(f"Failed to open camera at index {camera_index}")
            self.detector_view.display_console_output(f"Failed to open camera at index {camera_index}")
            return

        self.camera_feed_active = True
        threading.Thread(target=self._capture_frames, daemon=True).start()

    def stop_camera_feed(self):
        self.camera_feed_active = False
        if self.cap:
            self.cap.release()
            self.cap = None
        print("Camera feed stopped.")
        self.detector_view.display_console_output("Flujo de video detenido.")

    def _capture_frames(self):
        while self.camera_feed_active and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            _, buffer = cv2.imencode('.jpg', frame)
            img_data = buffer.tobytes()
            img_base64 = base64.b64encode(img_data).decode("utf-8")

            self.detector_view.update_camera_feed(img_base64)

        self.cap.release()  

    def handle_iniciar_proceso(self):
        self.detector_view.show_loading(True)
        threading.Thread(target=self.iniciar_proceso_thread).start()

    def iniciar_proceso_thread(self):
        try:
            self.iniciar_proceso()
        finally:
            self.detector_view.show_loading(False)
            
    def get_next_image_index(self):
        """Obtiene el índice más alto de las imágenes existentes y devuelve el siguiente índice disponible."""
        existing_images = glob.glob(os.path.join(self.detector_view.capture_path, "captureImage*.png"))
        if not existing_images:
            return 1  # No hay imágenes, empezar desde 1

        # Extraer el número de cada imagen y obtener el máximo
        max_index = max(
            int(os.path.splitext(os.path.basename(img))[0].replace("captureImage", ""))
            for img in existing_images
        )
        return max_index + 1  # Siguiente índice disponible
    
    def iniciar_proceso(self):
        # Inicia el proceso enviando "iniciar" al Arduino
        self.arduino.serial_connection.write(b'iniciar\n')
        self.detector_view.display_console_output("Enviado: iniciar")
        img_index = self.get_next_image_index()
        
        # Ruta de captura de imágenes
        current_path = os.path.abspath(__file__)
        root_path = os.path.dirname(os.path.dirname(current_path))
        capture_path = os.path.join(root_path, "src", "capture_images")
        result_path = os.path.join(root_path, "src", "result_images")
        
        # Definir un índice de imagen para el nombre de archivo
        #img_index = 1
        # Lista para almacenar las predicciones
        predictions_list = []

        # Espera la respuesta "escanear" para tomar la primera foto
        if self.esperar_respuesta("escanear"):
            self.tomar_foto_y_guardar(capture_path, f"captureImage{img_index}.png")
            self.prediction = detect_tomato(os.path.join(capture_path, f"captureImage{img_index}.png"), self.model, os.path.join(result_path, f"captureImage{img_index}_detection.png"))
            predictions_list.append(self.prediction)
            self.detector_view.update_images(os.path.join(result_path, f"captureImage{img_index}_detection.png"), self.prediction)
            self.arduino.serial_connection.write(b'foto1\n')
            self.detector_view.display_console_output("Enviado: foto1")
            img_index += 1

        # Espera la respuesta "giro90" para tomar la segunda foto
        if self.esperar_respuesta("giro90"):
            self.tomar_foto_y_guardar(capture_path, f"captureImage{img_index}.png")
            self.prediction = detect_tomato(os.path.join(capture_path, f"captureImage{img_index}.png"), self.model, os.path.join(result_path, f"captureImage{img_index}_detection.png"))
            predictions_list.append(self.prediction)
            self.detector_view.update_images(os.path.join(result_path, f"captureImage{img_index}_detection.png"), self.prediction)
            self.arduino.serial_connection.write(b'foto2\n')
            self.detector_view.display_console_output("Enviado: foto2")
            img_index += 1

        # Espera la respuesta "giro180" para tomar la tercera foto
        if self.esperar_respuesta("giro180"):
            self.tomar_foto_y_guardar(capture_path, f"captureImage{img_index}.png")
            self.prediction = detect_tomato(os.path.join(capture_path, f"captureImage{img_index}.png"), self.model, os.path.join(result_path, f"captureImage{img_index}_detection.png"))
            predictions_list.append(self.prediction)
            self.detector_view.update_images(os.path.join(result_path, f"captureImage{img_index}_detection.png"), self.prediction)
            self.arduino.serial_connection.write(b'foto3\n')
            self.detector_view.display_console_output("Enviado: foto3")
            img_index += 1

        # Espera la respuesta "giro270" para tomar la cuarta foto
        if self.esperar_respuesta("giro270"):
            self.tomar_foto_y_guardar(capture_path, f"captureImage{img_index}.png")
            self.prediction = detect_tomato(os.path.join(capture_path, f"captureImage{img_index}.png"), self.model, os.path.join(result_path, f"captureImage{img_index}_detection.png"))
            predictions_list.append(self.prediction)
            self.detector_view.update_images(os.path.join(result_path, f"captureImage{img_index}_detection.png"), self.prediction)
            self.arduino.serial_connection.write(b'foto4\n')
            self.detector_view.display_console_output("Enviado: foto4")
        print(f"este es mi predictionlist: {predictions_list}")
        # Espera la respuesta "resultado" para enviar el mensaje final
        if self.esperar_respuesta("resultado"):
        # Verificar que predictions_list no esté vacía
            if predictions_list:
                # Contar ocurrencias de cada predicción en la lista
                count = Counter(predictions_list)

                # Asegurarse de que hay al menos un elemento en el contador
                if count:
                    # Obtener la predicción más frecuente y su número de ocurrencias
                    most_common_prediction, common_count = count.most_common(1)[0]

                    # Si hay un empate o la predicción más común no es suficiente, selecciona la de mayor confianza
                    if common_count == 1 or common_count < len(predictions_list) / 2:
                        # Ordenar por porcentaje de confianza y seleccionar el valor con mayor confianza
                        most_common_prediction = max(
                            predictions_list,
                            key=lambda x: float(x.split("con")[1].strip('%'))
                        )
                else:
                    most_common_prediction = "Sin resultados"  # Valor por defecto si no hay predicciones válidas
            else:
                most_common_prediction = "Sin resultados"  # Valor por defecto si predictions_list está vacía

            # Generar el mensaje de resultado y actualizar la vista
            resultado_msg = f"resultado: {most_common_prediction}"
            self.detector_view.update_result(most_common_prediction)

            # Enviar el resultado al Arduino
            self.arduino.serial_connection.write(resultado_msg.encode())
            self.detector_view.display_console_output(f"Enviado: {resultado_msg}")

    def esperar_respuesta(self, respuesta_esperada, timeout=10):
        """Espera una respuesta específica del Arduino con un timeout."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.arduino.serial_connection.in_waiting > 0:
                response = self.arduino.serial_connection.readline().decode().strip()
                print(f"Arduino respondió: {response}")
                if respuesta_esperada in response:
                    self.detector_view.display_console_output(f"Arduino respondió: {response}")
                    return True
        self.detector_view.display_console_output(f"Error: No se recibió la respuesta esperada '{respuesta_esperada}' del Arduino.")
        return False

    def tomar_foto_y_guardar(self, path, filename):
        """Toma una foto de la cámara y la guarda en la ruta especificada."""
        if self.camera_feed_active:
            self.camera_feed_active = False
            time.sleep(1)  # Pequeña pausa para liberar la cámara
        if self.camera_feed_active:
            print("Camera feed is already active.")
            return

        selected_camera_index = self.detector_view.dropdown_cameras.value
        if selected_camera_index is None:
            print("No camera selected.")
            self.detector_view.display_console_output("Seleccione una cámara para iniciar.")
            return

        camera_index = int(selected_camera_index.split()[-1])
        # Asegúrate de que la cámara esté configurada y abierta
        if not self.cap or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(camera_index)  # Ajusta el índice de cámara si es necesario

        ret, frame = self.cap.read()
        if ret:
            # Guarda la imagen en la ruta especificada
            full_path = os.path.join(path, filename)
            cv2.imwrite(full_path, frame)
            self.detector_view.display_console_output(f"Foto guardada: {full_path}")
        else:
            self.detector_view.display_console_output("Error: No se pudo capturar la imagen.")
            
        # Reiniciar el feed de video después de la captura
        self.camera_feed_active = True
        threading.Thread(target=self._capture_frames, daemon=True).start()