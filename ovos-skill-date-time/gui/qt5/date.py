import flet as ft

def get_view(page, message_store):
    # Specificeer het namespace dat overeenkomt met de ontvangen data
    namespace = "skill-ovos-date-time.openvoiceos"
    
    # Controleer of het namespace in message_store zit
    if namespace in message_store:
        # Stel de datum weer samen uit de beschikbare gegevens
        date_display = (
            f"{message_store[namespace].get('weekday_string', '')}, "
            f"{message_store[namespace].get('daymonth_string', '')} "
            f"{message_store[namespace].get('year_string', '')}"
        ).strip()
    else:
        date_display = "Geen datum ontvangen."

    # Maak de view met de opgehaalde datum
    return ft.View(
        "/date",
        [
            ft.AppBar(title=ft.Text("Date"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Text(value=date_display),  # Toon de datum
            ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
        ],
    )
