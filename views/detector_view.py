import flet as ft
from utils.colors import ColorsUI

class DetectorView:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        self.status_label = ft.Text("Desconectado", color=ColorsUI.secundary_dark)
        self.dropdown_ports = ft.Dropdown()
        self.update_ports()

    def update_ports(self):
        ports = self.controller.arduino.get_ports()
        self.dropdown_ports.options = [ft.dropdown.Option(port) for port in ports]
    
    def set_status(self, status):
        self.status_label.value = status
        self.page.update()

    def build(self):
        return ft.View(
            "/detector",
            [
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Detector de Estados de Tomate", size=30, weight="bold", color=ColorsUI.primary),
                            ft.Image(src="assets/logo.png", width=200, height=200),
                            self.dropdown_ports,
                            ft.ElevatedButton(
                                text="Conectar Arduino",
                                bgcolor=ColorsUI.primary,
                                color="white",
                                on_click=lambda e: self.controller.conectar_arduino()
                            ),
                            self.status_label,
                            ft.Row(
                                controls=[
                                    ft.Text("Label 1", color=ColorsUI.secundary_dark),
                                    ft.Text("Label 2", color=ColorsUI.secundary_dark),
                                    ft.Text("Label 3", color=ColorsUI.secundary_dark),
                                    ft.Text("Label 4", color=ColorsUI.secundary_dark),
                                ]
                            ),
                            ft.ElevatedButton(text="Iniciar", bgcolor=ColorsUI.primary, color="white"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    bgcolor=ColorsUI.background,  # Aplica el fondo al Container
                    padding=20,
                    alignment=ft.alignment.center,
                )
            ]
        )
