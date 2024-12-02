from __future__ import annotations
import flet as ft
from ovos_gui_client import global_client

# Main Flet app setup
def main(page: ft.Page):
    page.title = "OVOS Flet GUI client"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    global_client.register(page)

    # TODO: deregister upon destroying instance. How?
# Start the Flet app
ft.app(target=main)
