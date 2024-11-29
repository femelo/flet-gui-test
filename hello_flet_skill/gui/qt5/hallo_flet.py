import flet as ft

def get_view(page, message_store):  # Voeg message_store als extra argument toe
    # Gebruik message_store om het bericht weer te geven
    message_text = message_store.get('hallo_flet', 'Geen bericht ontvangen.')

    return ft.View(
        "/hallo_flet",
        [
            ft.AppBar(title=ft.Text("Flet Page"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Text(value=message_text),  # Toon de boodschap
            ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
        ],
    )

