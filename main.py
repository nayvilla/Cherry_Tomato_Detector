
import flet as ft
from controllers.controller import MainController
from util.colors import ColorsUI
from util.constants import AppConstants

def main(page: ft.Page):
    page.title = AppConstants.APP_TITLE
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ColorsUI.background
    page.theme_mode = ft.ThemeMode.LIGHT

    # Crear controlador principal
    controller = MainController(page)
    controller.show_bienvenida()

ft.app(target=main)
