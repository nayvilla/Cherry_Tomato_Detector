# models/arduino_model.py
import serial
import serial.tools.list_ports

class ArduinoModel:
    def __init__(self):
        self.serial_connection = None

    def get_ports(self):
        # Devuelve una lista de puertos COM disponibles
        return [port.device for port in serial.tools.list_ports.comports()]

    def connect(self, port):
        # Cierra cualquier conexión anterior
        self.close()
        try:
            self.serial_connection = serial.Serial(port, 9600, timeout=1)
            self.serial_connection.write(b'CONNECT\n')
            response = self.serial_connection.readline().decode().strip()
            return response == "Conectado"
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False


    def start_led(self):
        # Enciende el LED integrado
        if self.serial_connection:
            self.serial_connection.write(b'START\n')
            return self.serial_connection.readline().decode().strip()

    def stop_led(self):
        # Apaga el LED integrado
        if self.serial_connection:
            self.serial_connection.write(b'STOP\n')
            return self.serial_connection.readline().decode().strip()

    def close(self):
        # Cierra la conexión serial
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
