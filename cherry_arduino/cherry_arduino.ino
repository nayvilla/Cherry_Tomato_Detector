// Código para Arduino Mega

void setup() {
  Serial.begin(9600);      // Inicializar comunicación serial a 9600 baudios
  pinMode(LED_BUILTIN, OUTPUT); // LED integrado como salida
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Leer el comando hasta el final de la línea

    if (command == "CONNECT") {
      Serial.println("Conectado"); // Responde con "Conectado"
    }
    else if (command == "START") {
      digitalWrite(LED_BUILTIN, HIGH); // Enciende el LED
      Serial.println("LED Encendido");
    }
    else if (command == "STOP") {
      digitalWrite(LED_BUILTIN, LOW); // Apaga el LED
      Serial.println("LED Apagado");
    }
  }
}
