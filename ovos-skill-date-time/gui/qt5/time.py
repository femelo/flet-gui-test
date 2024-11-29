import flet as ft

def get_view(page, message_store):
    # Specificeer het namespace dat overeenkomt met de ontvangen data
    namespace = "skill-ovos-date-time.openvoiceos"
    
    # Controleer of het namespace in message_store zit
    if namespace in message_store:
        # Haal de waarde van 'time_string' op uit de juiste namespace
        time_string = message_store[namespace].get("time_string", "Geen tijd ontvangen.")
    else:
        time_string = "Geen tijd ontvangen."
    
    # Maak de view met de opgehaalde tijd
    return ft.View(
        "/time",
        [
            ft.AppBar(title=ft.Text("Time"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Text(value=f"Tijd: {time_string}"),  # Toon de tijd
            ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
        ],
    )
