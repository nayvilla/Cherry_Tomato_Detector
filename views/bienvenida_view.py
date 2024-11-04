import flet as ft
from util.constants import AppConstants
from util.colors import ColorsUI

class BienvenidaView:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller

    def build(self):
        return ft.View(
            "/bienvenida",
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,  
                    expand=True,
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    AppConstants.APP_TITLE, 
                                    size=30, 
                                    weight="bold", 
                                    color=ColorsUI.secundary_dark,
                                ),
                                ft.Text(
                                    "Universidad Técnica de Ambato", 
                                    size=18, 
                                    color=ColorsUI.secundary_dark,
                                    weight="bold"
                                ),
                                ft.Image(
                                    src="assets/logo.png", 
                                    width=200, 
                                    height=200, 
                                    border_radius=15
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text("Integrantes:", size=18, color=ColorsUI.secundary_dark, weight="bold"),
                                        ft.Container(height=20),
                                        ft.Row(
                                            controls=[
                                                ft.Text(" ", size=18, color=ColorsUI.secundary_dark),
                                                ft.Text("Nombre1 Apellido1,", size=17, color=ColorsUI.secundary_dark,)
                                            ],
                                            spacing=5,
                                            alignment=ft.MainAxisAlignment.CENTER
                                        ),
                                        ft.Row(
                                            controls=[
                                                ft.Text(" ", size=18, color=ColorsUI.secundary_dark),
                                                ft.Text("Nombre2 Apellido2", size=17, color=ColorsUI.secundary_dark,)
                                            ],
                                            spacing=5,
                                            alignment=ft.MainAxisAlignment.CENTER
                                        ),
                                    ],
                                    spacing=2, 
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Text("Nivel:", size=18, color=ColorsUI.secundary_dark, weight="bold"),
                                        ft.Text("2 Semestre", size=17)
                                    ],
                                    spacing=5,
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Text("Curso:", size=18, color=ColorsUI.secundary_dark, weight="bold"),
                                        ft.Text("A", size=17)
                                    ],
                                    spacing=5,
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
                                ft.Container(height=10),
                                ft.ElevatedButton(
                                    content=ft.Text("Entrar", size=20),
                                    bgcolor=ColorsUI.primary,
                                    color="white",
                                    on_click=lambda e: self.controller.show_detector(),
                                    width=200,
                                    height=50
                                ),
                                ft.Container(height=10),
                                ft.Text(
                                    AppConstants.COPYRIGHT_TEXT, 
                                    size=14, 
                                    italic=True, 
                                    color=ColorsUI.secundary
                                ),
                                
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=15  # Ajuste del espacio general entre los elementos
                        ),
                        bgcolor=ColorsUI.secundary, 
                        alignment=ft.alignment.center,
                        width=700,  # Limita el ancho máximo a 700 píxeles
                        border_radius=15,
                        padding=ft.padding.only(left=20, top=10, right=20, bottom=10)
                    )
                )
            ]
        )
