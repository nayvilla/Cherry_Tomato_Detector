# controller.py
import flet as ft
import cv2
import base64
import threading

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
        self.cap = None  # Variable to store the camera capture object
        self.camera_feed_active = False  # Flag to track if the camera feed is active

    def show_bienvenida(self):
        self.page.window_width = 750
        self.page.window_height = 700 
        self.page.views.clear()
        self.page.views.append(self.bienvenida_view.build())
        self.page.update()

    def show_detector(self):
        self.page.window_width = 1000
        self.page.window_height = 1000
        self.page.views.clear()
        self.page.views.append(self.detector_view.build())
        self.page.update()

    def conectar_arduino(self):
        selected_port = self.detector_view.dropdown_ports.value
        if selected_port and self.arduino.connect(selected_port):
            self.detector_view.set_status("Conectado")
            self.detector_view.display_console_output("Arduino conectado")
        else:
            self.detector_view.set_status("Error al conectar")
            self.detector_view.display_console_output("Error al conectar al Arduino")

    def start_led(self):
        response = self.arduino.start_led()
        if response:
            self.detector_view.display_console_output(response)

    def stop_led(self):
        response = self.arduino.stop_led()
        if response:
            self.detector_view.display_console_output(response)

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

        # Get the selected camera index from the dropdown
        selected_camera_index = self.detector_view.dropdown_cameras.value
        if selected_camera_index is None:
            print("No camera selected.")
            self.detector_view.display_console_output("Seleccione una cámara para iniciar.")
            return

        # Convert selected camera index to integer
        camera_index = int(selected_camera_index)

        # Open the camera
        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_MSMF if camera_index == 0 else cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            print(f"Failed to open camera at index {camera_index}")
            self.detector_view.display_console_output(f"Failed to open camera at index {camera_index}")
            return

        self.camera_feed_active = True
        threading.Thread(target=self._capture_frames, daemon=True).start()

    def stop_camera_feed(self):
        # Stop the camera feed
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

            # Encode the frame as JPEG, then convert to base64
            _, buffer = cv2.imencode('.jpg', frame)
            img_data = buffer.tobytes()
            img_base64 = base64.b64encode(img_data).decode("utf-8")

            # Update the image in DetectorView
            self.detector_view.update_camera_feed(img_base64)

        self.cap.release()  # Release the camera when loop exits
