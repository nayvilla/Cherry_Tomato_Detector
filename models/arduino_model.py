import serial
import serial.tools.list_ports

class ArduinoModel:
    def __init__(self):
        self.connection = None

    def get_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def connect(self):
        ports = self.get_ports()
        if ports:
            self.connection = serial.Serial(ports[0], 9600)
            return True
        return False
