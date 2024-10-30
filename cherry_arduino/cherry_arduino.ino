// Define states
enum State {
  WAIT_FOR_START,
  WAIT_FOR_FOTO1,
  WAIT_FOR_FOTO2,
  WAIT_FOR_FOTO3,
  WAIT_FOR_FOTO4,
  WAIT_FOR_RESULT
};

// Initialize state
State currentState = WAIT_FOR_START;
String receivedData = "";

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Check if data is available on the Serial
  if (Serial.available() > 0) {
    receivedData = Serial.readStringUntil('\n');
    receivedData.trim();  // Remove any extra whitespace or newlines
  }

  // Main state machine
  switch (currentState) {
    case WAIT_FOR_START:
      if (receivedData == "iniciar") {
        delay(2000);  // Wait 2 seconds
        Serial.println("escanear");
        currentState = WAIT_FOR_FOTO1;
      }
      break;

    case WAIT_FOR_FOTO1:
      if (receivedData == "foto1") {
        delay(2000);  // Wait 2 seconds
        Serial.println("giro90");
        currentState = WAIT_FOR_FOTO2;
      }
      break;

    case WAIT_FOR_FOTO2:
      if (receivedData == "foto2") {
        delay(2000);  // Wait 2 seconds
        Serial.println("giro180");
        currentState = WAIT_FOR_FOTO3;
      }
      break;

    case WAIT_FOR_FOTO3:
      if (receivedData == "foto3") {
        delay(2000);  // Wait 2 seconds
        Serial.println("giro270");
        currentState = WAIT_FOR_FOTO4;
      }
      break;

    case WAIT_FOR_FOTO4:
      if (receivedData == "foto4") {
        delay(2000);  // Wait 2 seconds
        Serial.println("resultado");
        currentState = WAIT_FOR_RESULT;
      }
      break;

    case WAIT_FOR_RESULT:
      // Wait for any input that starts with "resultado"
      if (receivedData.startsWith("resultado")) {
        Serial.println("Proceso completado. Listo para reiniciar."); // Confirm completion
        currentState = WAIT_FOR_START;  // Reset to start to allow re-triggering
      }
      break;
  }

  // Clear the received data after processing
  receivedData = "";
}
