# models/camera_model.py
import cv2

class CameraModel:
    def get_cameras(self):
        available_cameras = []
        index = 0  # Comenzar con el primer índice de cámara
        
        # Detectar cámaras disponibles de manera dinámica
        while True:
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                available_cameras.append(f"Camera {index}")
                cap.release()
            else:
                cap.release()
                break
            index += 1  # Avanzar al siguiente índice
        
        return available_cameras

    def open_camera(self, index=0):
        """Abre la cámara y devuelve el flujo de video."""
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            print("No se pudo abrir la cámara")
            return None

        return cap
