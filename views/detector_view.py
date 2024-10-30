import flet as ft
from utils.colors import ColorsUI
from utils.constants import AppConstants

class DetectorView:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        self.status_label = ft.Text("Desconectado", color=ColorsUI.secundary_dark)
        self.dropdown_ports = ft.Dropdown()
        self.dropdown_cameras = ft.Dropdown()
        self.console_output = ft.TextField(read_only=True, multiline=True, height=100, border_color=ColorsUI.primary)
        self.result_label = ft.Text("AQUI ESTA EL RESULTADO", size=24, weight="bold", color=ColorsUI.primary)
        self.camera_feed = ft.Image(src="path/to/placeholder_image.jpg", width=300, height=200)
        self.update_ports()
        self.update_cameras()

    def update_ports(self):
        ports = self.controller.arduino.get_ports()
        self.dropdown_ports.options = [ft.dropdown.Option(port) for port in ports]

    def update_cameras(self):
        cameras = self.controller.camera.get_cameras()
        self.dropdown_cameras.options = [ft.dropdown.Option(camera) for camera in cameras]

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

    def build(self):
        # Create image columns with different images and text
        image_columns = [
            ft.Column(
                [
                    ft.Container(
                        content=ft.Image(src="path/to/image1.jpg", width=200, height=200),
                        border=ft.border.all(1, ColorsUI.secundary_dark),
                        padding=5,
                        bgcolor=ColorsUI.background, 
                        border_radius=15
                    ),
                    ft.Container(
                        ft.Text("Texto imagen 1", color=ColorsUI.secundary_dark),
                        alignment=ft.alignment.center,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Column(
                [
                    ft.Container(
                        content=ft.Image(src="path/to/image2.jpg", width=200, height=200),
                        border=ft.border.all(1, ColorsUI.secundary_dark),
                        padding=5,
                        bgcolor=ColorsUI.background, 
                        border_radius=15
                    ),
                    ft.Container(
                        ft.Text("Texto imagen 2", color=ColorsUI.secundary_dark),
                        alignment=ft.alignment.center,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Column(
                [
                    ft.Container(
                        content=ft.Image(src="path/to/image3.jpg", width=200, height=200),
                        border=ft.border.all(1, ColorsUI.secundary_dark),
                        padding=5,
                        bgcolor=ColorsUI.background, 
                        border_radius=15
                    ),
                    ft.Container(
                        ft.Text("Texto imagen 3", color=ColorsUI.secundary_dark),
                        alignment=ft.alignment.center,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Column(
                [
                    ft.Container(
                        content=ft.Image(src="path/to/image4.jpg", width=200, height=200),
                        border=ft.border.all(1, ColorsUI.secundary_dark),
                        padding=5,
                        bgcolor=ColorsUI.background, 
                        border_radius=15
                    ),
                    ft.Container(
                        ft.Text("Texto imagen 4", color=ColorsUI.secundary_dark),
                        alignment=ft.alignment.center,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ]

        return ft.View(
            "/detector",
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
                                        on_click=lambda e: self.controller.conectar_arduino()
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
                                                on_click=lambda e: self.controller.start_camera_feed()
                                            ),
                                            ft.ElevatedButton(
                                                text="Detener",
                                                bgcolor=ColorsUI.primary,
                                                color="white",
                                                on_click=lambda e: self.controller.stop_camera_feed()
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
                    ft.Row(
                        image_columns,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10
                    ),
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
            padding=20,
            bgcolor=ColorsUI.background,
        )
