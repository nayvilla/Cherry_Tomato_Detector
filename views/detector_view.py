import glob
import os
import flet as ft
from util.colors import ColorsUI
from util.constants import AppConstants
from model.arduino_model import ArduinoModel

class DetectorView:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        self.arduino = ArduinoModel()
        self.status_label = ft.Text("Desconectado", color=ColorsUI.secundary_dark)
        self.dropdown_ports = ft.Dropdown()
        self.dropdown_cameras = ft.Dropdown()
        self.console_output = ft.TextField(read_only=True, multiline=True, height=100, border_color=ColorsUI.primary)
        self.result_label = ft.Text("AQUI ESTA EL RESULTADO", size=24, weight="bold", color=ColorsUI.primary)
        self.camera_feed = ft.Image(src="path/to/placeholder_image.jpg", width=300, height=200)
        self.update_ports()
        self.update_cameras()
        self.loading_modal = ft.AlertDialog(
            modal=True,
            content=ft.Column(
                [
                    ft.Text("Cargando...", size=20, weight="bold"),
                    ft.ProgressBar(width=300, height=20),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                height=200, 
            ),
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        self.current_path = os.path.abspath(__file__)
        self.root_path = os.path.dirname(os.path.dirname(self.current_path))
        self.capture_path = os.path.join(self.root_path, "src", "capture_images")
        self.clear_images()
        self.image_container = ft.Row(spacing=10, alignment=ft.MainAxisAlignment.CENTER)
    
    def show_loading(self, show):
        """Muestra u oculta el modal de carga."""
        if show:
            self.page.dialog = self.loading_modal
            self.loading_modal.open = True
        else:
            self.loading_modal.open = False
        #self.update_images()
        self.page.update()

    def update_ports(self):
        ports = self.arduino.get_ports()
        #print(f"Hay estos puertos: {ports}")
        self.dropdown_ports.options = [ft.dropdown.Option(port) for port in ports]
        self.page.update()

    def update_cameras(self):
        cameras = self.controller.camera.get_cameras()
        self.dropdown_cameras.options = [ft.dropdown.Option(camera) for camera in cameras]
        self.page.update()

    def set_status(self, status):
        self.status_label.value = status
        self.page.update()

    def update_camera_feed(self, img_base64):
        if img_base64:
            self.camera_feed.src_base64 = img_base64
            self.page.update()

    def display_console_output(self, message):
        self.console_output.value += message + "\n"
        self.page.update()
        
    def clear_images(self):
        """Elimina todas las imágenes .png en el directorio de captura."""
        for file_path in glob.glob(os.path.join(self.capture_path, "*.png")):
            try:
                os.remove(file_path)
                print(f"Archivo eliminado: {file_path}")
            except Exception as e:
                print(f"Error al eliminar {file_path}: {e}")

    def create_image_column(self, image_path):
        if os.path.exists(image_path):
            print(f"Path detectado imagen: {image_path}")
            return ft.Container(
                content=ft.Image(src=image_path, width=200, height=200),
                border=ft.border.all(1, ColorsUI.secundary_dark),
                padding=5,
                bgcolor=ColorsUI.background,
                border_radius=15
            )
        else:
            print(f"La imagen no existe: {image_path}")
            return None

    def update_images(self, image_path):    
        if len(self.image_container.controls) >= 4:
            self.image_container.controls.clear()
        
        new_image = self.create_image_column(image_path)
        if new_image:
            self.image_container.controls.append(new_image)
        self.image_container.update()
        self.page.update()


    def build(self):

        return ft.View(
            "/detector",
            [
                ft.Column(
                    [
                        # Title
                        ft.Container(
                            ft.Text(AppConstants.APP_TITLE, size=30, weight="bold", color=ColorsUI.primary),
                            alignment=ft.alignment.center,
                            bgcolor=ColorsUI.background, 
                            padding=10,
                        ),
                        
                        # Row for COM Port selection and Arduino Console output
                        ft.Container(
                            ft.Row(
                                [
                                    # Left Column: COM Port Dropdown, Connect Button, Status, Refresh Button
                                    ft.Column(
                                        [
                                            ft.Text("Seleccionar Puerto COM", color=ColorsUI.secundary_dark, weight="bold"),
                                            ft.Row([
                                                ft.ElevatedButton(
                                                    text=' ',
                                                    icon=ft.icons.REFRESH,
                                                    on_click=lambda e: self.update_ports()
                                                ),
                                                self.dropdown_ports                                    
                                            ]),
                                            ft.ElevatedButton(
                                                text="Conectar Arduino",
                                                bgcolor=ColorsUI.primary,
                                                color="white",
                                                on_click=lambda e: self.controller.handle_conectar_arduino()
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.START,
                                        spacing=10
                                    ),
                                    # Right Column: Console Output
                                    ft.Column(
                                        [
                                            ft.Text("Consola Arduino", color=ColorsUI.secundary_dark, weight="bold"),
                                            ft.Container(
                                                self.console_output,
                                                border=ft.border.all(1, ColorsUI.primary),
                                                bgcolor=ColorsUI.background, 
                                                width=400,
                                                height=100,
                                                border_radius=15
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.START,
                                        spacing=10
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=20
                            ),
                            alignment=ft.alignment.center,
                            bgcolor=ColorsUI.secundary, 
                            padding=10,
                            border_radius=15
                        ),
                        # Row for Camera selection and Camera feed
                        ft.Container(
                            ft.Row(
                                [
                                    # Left Column: Camera Dropdown, Start/Stop Buttons
                                    ft.Column(
                                        [
                                            ft.Text("Seleccionar Cámara", color=ColorsUI.secundary_dark, weight="bold"),
                                            ft.Row([
                                                ft.ElevatedButton(
                                                    text=' ',
                                                    icon=ft.icons.REFRESH,
                                                    on_click=lambda e: self.update_cameras()
                                                ),
                                                self.dropdown_cameras,
                                            ]),
                                            ft.Row(
                                                [
                                                    ft.ElevatedButton(
                                                        text="Iniciar",
                                                        bgcolor=ColorsUI.primary,
                                                        color="white",
                                                        on_click=lambda e: self.controller.handle_iniciar_proceso()
                                                    ),
                                                    ft.ElevatedButton(
                                                        text="Detener",
                                                        bgcolor=ColorsUI.primary,
                                                        color="white",
                                                        on_click=lambda e: self.controller.stop_camera_feed()
                                                    ),
                                                    ft.ElevatedButton(
                                                        text="Probar Cámara",
                                                        bgcolor=ColorsUI.primary,
                                                        color="white",
                                                        on_click=lambda e: self.controller.start_camera_feed()
                                                    ),
                                                ],
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                spacing=10
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.START,
                                        spacing=10
                                    ),
                                    # Right Column: Camera feed
                                    ft.Container(
                                        content=self.camera_feed,
                                        border=ft.border.all(1, ColorsUI.primary),
                                        alignment=ft.alignment.center,
                                        bgcolor=ColorsUI.primary, 
                                        padding=10,
                                        border_radius=15,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=20
                            ),
                            alignment=ft.alignment.center,
                            bgcolor=ColorsUI.secundary, 
                            padding=10,
                            border_radius=15
                        ),

                        ft.Container(
                            # Row for Image Grid
                            self.image_container,
                            alignment=ft.alignment.center,
                            bgcolor=ColorsUI.secundary,
                            padding=10,
                            border_radius=15
                        ),
                        
                        # Result Label Section
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Resultados:", color=ColorsUI.secundary_dark, weight="bold"),
                                    ft.Container(
                                        self.result_label,
                                        border=ft.border.all(2, ColorsUI.secundary_dark),
                                        bgcolor=ColorsUI.background,
                                        padding=10,
                                        alignment=ft.alignment.center,
                                        width=500,
                                        height=70,
                                        border_radius=15,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            padding=10,
                            border_radius=15,
                            bgcolor=ColorsUI.secundary,
                            alignment=ft.alignment.center
                        ),
                    ],
                    scroll="auto",  # Habilita el scroll automático en toda la pantalla
                    expand=True
                ),
                
            ],
            padding=20,
            bgcolor=ColorsUI.background,
        )
