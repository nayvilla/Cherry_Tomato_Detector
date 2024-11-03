# models/arduino_model.py
import time
import serial
import serial.tools.list_ports

class ArduinoModel:
    def __init__(self):
        self.serial_connection = None

    def get_ports(self):
        # Devuelve una lista de puertos COM disponibles
        return [port.device for port in serial.tools.list_ports.comports()]

    def connect(self, port):
        self.close()
        try:
            self.serial_connection = serial.Serial(port, 9600, timeout=2)
            time.sleep(2)
            self.serial_connection.reset_input_buffer()
            self.serial_connection.write(b'CONNECT\n')
            time.sleep(2)
            response = ""
            start_time = time.time()
            while (time.time() - start_time) < 3:  
                if self.serial_connection.in_waiting > 0:
                    response += self.serial_connection.readline().decode().strip()
                    if "Conectado" in response:
                        break
            print(f"Esta es la response: {response}")
            return "Conectado" in response
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
