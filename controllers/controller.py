# controller.py
import flet as ft
import cv2
import base64

from views.bienvenida_view import BienvenidaView
from views.detector_view import DetectorView
from models.arduino_model import ArduinoModel
from models.camera_model import CameraModel


class MainController:
    def __init__(self, page):
        self.page = page
        self.arduino = ArduinoModel()
        self.camera = CameraModel()
        self.bienvenida_view = BienvenidaView(page, self)
        self.detector_view = DetectorView(page, self)
        self.update_camera_list()
        self.cap = None  # Variable para almacenar el objeto de captura de la cámara

    def show_bienvenida(self):
        self.page.window_width = 750
        self.page.window_height = 700 
        self.page.views.clear()
        self.page.views.append(self.bienvenida_view.build())
        self.page.update()

    def show_detector(self):
        self.page.window_width = 1000
        self.page.window_height = 800
        self.page.views.clear()
        self.page.views.append(self.detector_view.build())
        self.page.update()

    def conectar_arduino(self):
        if self.arduino.connect():
            self.detector_view.set_status("Conectado")
        else:
            self.detector_view.set_status("Error al conectar")

    def update_camera_list(self):
        cameras = self.camera.get_cameras()
        self.detector_view.dropdown_cameras.options = [
            ft.dropdown.Option(camera) for camera in cameras
        ]
        self.page.update()

        def start_camera_feed(self):
            # Iniciar el flujo de video desde la cámara
            self.cap = self.camera.open_camera(0)
            if self.cap is None:
                print("No se pudo iniciar el flujo de video")
                return

            # Bucle para capturar y actualizar frames
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("No se pudo capturar el frame de la cámara")
                    break
                
                # Convertir el frame a JPEG y luego a bytes
                _, buffer = cv2.imencode('.jpg', frame)
                img_data = buffer.tobytes()

                # Convertir los bytes de la imagen a base64
                img_base64 = base64.b64encode(img_data).decode("utf-8")

                # Actualizar la imagen en DetectorView con base64
                self.detector_view.update_camera_feed(img_base64)

                # Pausa para permitir actualización de la UI
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            self.cap.release()  # Liberar la cámara al salir
