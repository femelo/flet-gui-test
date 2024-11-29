import flet as ft
import datetime
import time
import threading
import json
import os
from websocket import create_connection

# Achtergrondafbeelding
ACHTERGROND_AFBEELDING = "https://cdn.pixabay.com/photo/2016/06/02/02/33/triangles-1430105_1280.png?text=Achtergrond+1"

# Gedeelde structuur om berichten per namespace op te slaan
message_store = {}

# Verbinden met OVOS-GUI WebSocket
def connect_to_ovos_gui():
    try:
        ws = create_connection("ws://localhost:18181/gui")  # Gebruik de juiste host, poort en route
        print("Verbonden met OVOS-GUI WebSocket")
        return ws
    except Exception as e:
        print(f"Fout bij verbinden met OVOS-GUI: {e}")
        return None


def log_message(message):
    """
    Logt berichten naar de terminal.
    """
    print(message)


def construct_url(namespace: str, page_name: str) -> str:
    """
    Construeert de URL op basis van het gegeven namespace en page_name.
    """
    user_home = os.path.expanduser("~")  # Haal de home directory op
    url = os.path.join(user_home, ".cache", "ovos_gui", namespace, "qt5", f"{page_name}.py")
    return url

def process_gui_message(data, page, message_store):
    try:
        msg_type = data.get("type")
        namespace = data.get("namespace")
        event_name = data.get("event_name", "")
        payload = data.get("data", {})
        property_name = data.get("property")
        position = data.get("position")
        values = data.get("values")

        log_message(f"Inkomend bericht: {msg_type}")
        log_message(f"Volledige data: {json.dumps(data)}")
        
        # Specifieke verwerking voor mycroft.events.triggered
        if msg_type == "mycroft.events.triggered" and event_name == "recognizer_loop:wakeword":
            log_message("Wakeword gedetecteerd! Toon gloei-effect.")
        
            # Activeer het gloei-effect met animatie alleen op rand en schaduw
            page.glow_container.border = ft.border.all(10, "rgba(255, 255, 255, 0.1)")  # Lichte, transparante rand
            page.glow_container.shadow = ft.BoxShadow(
                spread_radius=60,  # Meer spreiding voor zachtheid
                blur_radius=150,  # Zacht verloop
                color="rgba(255, 255, 255, 0.3)"  # Licht doorschijnend wit gloei-effect
            )
            page.glow_container.opacity = 0.6  # Maak de container zelf zichtbaar met een lichte transparantie
            page.glow_container.visible = True
            page.update()
            
            # Verberg het gloei-effect na enkele seconden
            def hide_glow():
                time.sleep(3)  # Glow-effect blijft 3 seconden zichtbaar
                page.glow_container.border = ft.border.all(15, "transparent")
                page.glow_container.shadow = ft.BoxShadow(
                    spread_radius=50,
                    blur_radius=100,
                    color="transparent"  # Terug naar volledig transparant
                )
                page.glow_container.opacity = 0  # Maak de container weer volledig transparant
                page.glow_container.visible = False
                page.update()
            
            threading.Thread(target=hide_glow, daemon=True).start()


        # Verwerk "mycroft.session.set"
        if msg_type == "mycroft.session.set":
            for key, value in payload.items():
                if value:  # Negeer lege waarden
                    message_store.setdefault(namespace, {})[key] = value
                    log_message(f"Opgeslagen in '{namespace}': {key} = {value}")

                    # Update view als de huidige pagina overeenkomt met de namespace
                    if page.route == f"/{namespace}":
                        page.views[-1].controls[1].value = f"Ontvangen: {key} = {value}"
                        page.update()

        # Verwerk "mycroft.session.delete"
        elif msg_type == "mycroft.session.delete" and property_name:
            if namespace in message_store and property_name in message_store[namespace]:
                del message_store[namespace][property_name]
                log_message(f"Verwijderd uit '{namespace}': {property_name}")

                if page.route == f"/{namespace}":
                    page.views[-1].controls[1].value = f"Verwijderd: {property_name}"
                    page.update()

        # Verwerk "mycroft.session.list.insert"
        elif msg_type == "mycroft.session.list.insert" and isinstance(values, list):
            list_data = message_store.setdefault(namespace, {}).setdefault(property_name, [])
            for i, item in enumerate(values):
                insert_position = position + i if position is not None else len(list_data)
                list_data.insert(insert_position, item)
                log_message(f"Ingevoegd in '{namespace}.{property_name}' op positie {insert_position}: {item}")

        # Verwerk "mycroft.session.list.update"
        elif msg_type == "mycroft.session.list.update" and isinstance(values, list):
            list_data = message_store.get(namespace, {}).get(property_name, [])
            for i, item in enumerate(values):
                update_position = position + i if position is not None else i
                if update_position < len(list_data):
                    list_data[update_position] = item
                    log_message(f"Bijgewerkt in '{namespace}.{property_name}' op positie {update_position}: {item}")
                else:
                    log_message(f"Waarschuwing: Geen item op positie {update_position} in '{namespace}.{property_name}'")

        # Verwerk "mycroft.session.list.move"
        elif msg_type == "mycroft.session.list.move":
            list_data = message_store.get(namespace, {}).get(property_name, [])
            from_pos = data.get("from")
            to_pos = data.get("to")
            items_number = data.get("items_number", 1)
            if from_pos is not None and to_pos is not None:
                for _ in range(items_number):
                    if from_pos < len(list_data):
                        item = list_data.pop(from_pos)
                        list_data.insert(to_pos, item)
                        log_message(f"Verplaatst in '{namespace}.{property_name}' van {from_pos} naar {to_pos}: {item}")
                        to_pos += 1

        # Verwerk "mycroft.session.list.remove"
        elif msg_type == "mycroft.session.list.remove":
            list_data = message_store.get(namespace, {}).get(property_name, [])
            if position is not None:
                items_number = data.get("items_number", 1)
                for _ in range(items_number):
                    if position < len(list_data):
                        removed_item = list_data.pop(position)
                        log_message(f"Verwijderd uit '{namespace}.{property_name}' op positie {position}: {removed_item}")

        # Verwerk "mycroft.gui.list.insert"
        elif msg_type == "mycroft.gui.list.insert" and isinstance(payload, list):
            for item in payload:
                page_name = item.get("page")
                url = item.get("url")

                if url is None and page_name:
                    url = construct_url(namespace, page_name)
                    log_message(f"Geconstrueerde URL: {url}")
                    show_constructed_url_page(page, namespace, page_name, message_store)
                elif url:
                    log_message(f"Gevonden URL: {url}")
                    show_constructed_url_page(page, namespace, page_name, message_store)

        else:
            log_message(f"Onbekend of niet-ondersteund berichttype: {msg_type}")

    except Exception as e:
        log_message(f"Fout bij verwerken van bericht: {e}")


def show_constructed_url_page(page, namespace, page_name, message_store):
    """
    Toont een pagina gebaseerd op de geconstrueerde URL en de message_store.
    """
    # Voeg .py toe aan de geconstrueerde URL
    url = construct_url(namespace, page_name)
    log_message(f"Probeer pagina te laden van URL: {url}")

    try:
        # Controleer of het bestand bestaat
        if not os.path.exists(url):
            log_message(f"Bestand niet gevonden: {url}")
            raise FileNotFoundError

        # Dynamisch importeren van de view-module
        log_message(f"Bestand gevonden: {url}, probeer inhoud te laden als module.")
        import importlib.util

        spec = importlib.util.spec_from_file_location("dynamic_view", url)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # Voer het bestand uit als een Python-module

        # Controleer of de module de verwachte 'get_view' functie bevat
        if hasattr(module, "get_view"):
            log_message(f"Functie 'get_view' gevonden in {url}, probeer view te genereren.")
            constructed_view = module.get_view(page, message_store)  # Geef de message_store door
            log_message(f"View succesvol gegenereerd vanuit {url}.")

            page.views.clear()  # Verwijder huidige views
            page.views.append(constructed_view)  # Voeg de nieuwe view toe
            page.update()  # Update de pagina
            log_message(f"View succesvol geladen voor {url}")
        else:
            log_message(f"Functie 'get_view' niet gevonden in {url}")
            raise AttributeError(f"{url} bevat geen 'get_view' functie.")

    except FileNotFoundError:
        # Log en toon foutpagina als bestand niet gevonden is
        log_message(f"Error: Bestand niet gevonden voor URL: {url}")
        show_error_page(page, f"Kan de pagina niet laden: {url}")

    except AttributeError as e:
        # Log en toon foutpagina als de module niet de verwachte functie bevat
        log_message(f"Error: {e}")
        show_error_page(page, f"Onjuiste inhoud in {url}: {e}")

    except Exception as e:
        # Log en toon foutpagina voor andere fouten
        log_message(f"Onverwachte fout bij het laden van URL {url}: {e}")
        show_error_page(page, f"Onverwachte fout: {e}")



def show_error_page(page, error_message):
    """
    Toont een foutpagina met het opgegeven foutbericht.
    """
    error_view = ft.View(
        "/error",
        controls=[
            ft.Text(error_message, size=16, color="red"),
            ft.ElevatedButton(
                "Terug naar Home",
                on_click=lambda _: navigate_to_home(page),
            ),
        ],
    )
    page.views.clear()
    page.views.append(error_view)
    page.update()


# Functie voor navigatie naar home pagina
def navigate_to_home(page):
    # Functie voor het opnieuw laden van het homescreen
    update_home_page(page)


def update_home_page(page):
    tijd_text = ft.Text(size=150, color="white", weight=ft.FontWeight.BOLD)

    # Achtergrond instellingen
    achtergrond_container = ft.Container(
        expand=True,
        image_src=ACHTERGROND_AFBEELDING,
        image_fit=ft.ImageFit.COVER,
    )

    # Glow-effect container met animatie alleen op rand en schaduw, achtergrond blijft zichtbaar
    glow_container = ft.Container(
        expand=True,
        border=ft.border.all(5, "transparent"),  # Dunnere randen
        animate=ft.animation.Animation(800, "easeInOut"),
        shadow=ft.BoxShadow(
            spread_radius=30,  # Meer spreiding voor de schaduw
            blur_radius=80,  # Zachte overgang
            color="rgba(255, 0, 255, 0.7)"  # Glow-effect met een roze/gloeiende kleur
        ),
        visible=False,  # Glow-effect is standaard verborgen
        opacity=0.3,  # De container blijft transparant, achtergrond is zichtbaar
    )
    page.glow_container = glow_container  # Maak dit toegankelijk in de `page`-object

    overlay = ft.Container(
        content=ft.Column(
            [
                tijd_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.END,
            spacing=10,
        ),
        padding=20,
        alignment=ft.alignment.Alignment(1, -1),
    )

    home_view = ft.View(
        "/",
        controls=[
            ft.Stack([achtergrond_container, glow_container, overlay], expand=True),
        ],
    )
    page.views.clear()  # Verwijder oude views
    page.views.append(home_view)  # Voeg de home view toe
    page.update()  # Update de pagina

    # Bijwerken van tijd
    def update_time():
        while True:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            tijd_text.value = current_time
            page.update()
            time.sleep(1)

    threading.Thread(target=update_time, daemon=True).start()




# Luister naar GUI WebSocket
def listen_to_ovos_gui(ws, page, message_store):
    try:
        while True:
            response = ws.recv()  # Ontvang berichten van de WebSocket
            if response:
                data = json.loads(response)
                process_gui_message(data, page, message_store)  # Voeg message_store toe als argument
    except Exception as e:
        log_message(f"Fout bij ontvangen van bericht: {e}")



def main(page):
    page.title = "OVOS Homescreen"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    
    # Voeg een route handler toe om navigatie naar "/" te verwerken
    def route_handler(route):
        if route == "/":
            update_home_page(page)  # Laad de homepagina

    # Stel de route handler in
    page.on_route_change = lambda e: route_handler(e.route)

    # Start op de homepagina
    update_home_page(page)

    # Verbinding met WebSocket en luisteren naar berichten
    ws = connect_to_ovos_gui()
    if ws:
        threading.Thread(target=listen_to_ovos_gui, args=(ws, page, {}), daemon=True).start()


# Start de Flet app
ft.app(target=main)
