
from views.bienvenida_view import BienvenidaView
from views.detector_view import DetectorView
from models.arduino_model import ArduinoModel

class MainController:
    def __init__(self, page):
        self.page = page
        self.arduino = ArduinoModel()
        self.bienvenida_view = BienvenidaView(page, self)
        self.detector_view = DetectorView(page, self)

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
