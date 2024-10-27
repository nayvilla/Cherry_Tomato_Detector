import cv2

# Inicializar la cámara en el índice 0
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo abrir la cámara")
else:
    print("Cámara abierta. Presiona 'q' para salir.")

    # Bucle para mostrar el flujo de la cámara
    while True:
        ret, frame = cap.read()  # Leer un frame de la cámara
        if not ret:
            print("No se pudo recibir el frame de la cámara")
            break

        # Mostrar el frame en una ventana
        cv2.imshow("Cámara integrada", frame)

        # Salir del bucle al presionar la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar el objeto de captura y cerrar la ventana
    cap.release()
    cv2.destroyAllWindows()
