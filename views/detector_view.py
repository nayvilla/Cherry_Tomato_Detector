import flet as ft
from utils.colors import ColorsUI

class DetectorView:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        self.status_label = ft.Text("Desconectado", color=ColorsUI.secundary_dark)
        self.dropdown_ports = ft.Dropdown()
        self.dropdown_cameras = ft.Dropdown()
        self.console_output = ft.TextField(read_only=True, multiline=True, height=100)
        self.result_label = ft.Text("Resultado", size=24, weight="bold", color=ColorsUI.primary)
        
        # Imagen para mostrar el flujo de la cámara
        self.camera_feed = ft.Image(src="", width=400, height=300)

        self.update_ports()
        self.update_cameras()

    def update_ports(self):
        # Obtener y actualizar puertos desde el modelo Arduino
        ports = self.controller.arduino.get_ports()
        self.dropdown_ports.options = [ft.dropdown.Option(port) for port in ports]

    def update_cameras(self):
        # Obtener y actualizar la lista de cámaras disponibles
        cameras = self.controller.camera.get_cameras()
        self.dropdown_cameras.options = [ft.dropdown.Option(camera) for camera in cameras]

    def set_status(self, status):
        # Actualizar el estado de conexión
        self.status_label.value = status
        self.page.update()

    def update_camera_feed(self, img_base64):
        # Actualiza el contenido de la imagen con el nuevo frame de la cámara
        self.camera_feed.src_base64 = img_base64
        self.page.update()

    def build(self):
        # Construir la vista del detector
        return ft.View(
            "/detector",
            [
                ft.Text("Detector de Estados de Tomate", size=30, weight="bold", color=ColorsUI.primary),
                
                # Row for Camera selection and Camera output
                ft.Row(
                    [
                        # Column for Camera Dropdown
                        ft.Column(
                            [
                                ft.Text("Seleccionar Cámara", color=ColorsUI.secundary_dark),
                                self.dropdown_cameras,
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        # Column for Camera Feed (flujo de cámara en tiempo real)
                        ft.Container(
                            content=self.camera_feed,
                            alignment=ft.alignment.center,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                
                # Row for COM port selection and Arduino console output
                ft.Row(
                    [
                        # Column for COM port Dropdown, Connect button, and Status
                        ft.Column(
                            [
                                ft.Text("Seleccionar Puerto COM", color=ColorsUI.secundary_dark),
                                self.dropdown_ports,
                                ft.ElevatedButton(
                                    text="Conectar Arduino",
                                    bgcolor=ColorsUI.primary,
                                    color="white",
                                    on_click=lambda e: self.controller.conectar_arduino()
                                ),
                                self.status_label,
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        # Column for Console output from Arduino
                        ft.Column(
                            [
                                ft.Text("Consola Arduino", color=ColorsUI.secundary_dark),
                                self.console_output,
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                
                # Row for grid of labels and result label
                ft.Row(
                    [
                        # Grid layout for 8 labels
                        ft.Column(
                            [
                                ft.GridView(
                                    controls=[
                                        ft.Text(f"Label {i+1}", color=ColorsUI.secundary_dark) for i in range(8)
                                    ],
                                    runs_count=2,  # 2 columns
                                    spacing=5,     # Espacio entre etiquetas
                                )
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        # Result label for output
                        ft.Column(
                            [
                                self.result_label,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                
                # Start button
                ft.ElevatedButton(
                    text="Iniciar",
                    bgcolor=ColorsUI.primary,
                    color="white",
                    on_click=lambda e: self.controller.start_camera_feed()
                ),
            ],
            padding=20,
            bgcolor=ColorsUI.background,
        )
