import flet as ft
import requests
import datetime
import time
import threading
import logging
import json
from websocket import create_connection

# Background image
WALLPAPER = "https://cdn.pixabay.com/photo/2016/06/02/02/33/triangles-1430105_1280.png?text=Achtergrond+1"

# Connect to OVOS-GUI WebSocket
def connect_to_ovos_gui():
    try:
        ws = create_connection("ws://localhost:18181/gui")  # Use the correct host, port, and route
        print("Connected to OVOS-GUI WebSocket")
        return ws
    except Exception as e:
        print(f"Error connecting to OVOS-GUI: {e}")
        return None


# General processing of GUI messages
def process_gui_message(data, page, component_map):
    msg_type = data.get("type")
    namespace = data.get("namespace")

    if msg_type == "mycroft.session.set":
        session_data = data.get("data", {})
        handle_session_set(namespace, session_data, component_map, page)

    elif msg_type == "mycroft.events.triggered":
        event_name = data.get("event_name")
        parameters = data.get("data", {})
        handle_events_triggered(event_name, parameters, component_map, page)

    elif msg_type == "mycroft.gui.list.insert":
        if namespace == "hallo_flet":  # Check if the correct namespace is used
            page_name = data.get("data", [{}])[0].get("page")
            if page_name == "hello_world":
                # This should load the 'hello_world' page
                show_hello_world_page(page, f"{page_name}")
                
        elif namespace == "skill-ovos-date-time.openvoiceos":  # Specific skill
            page_name = data.get("data", [{}])[0].get("page", "unknown")
            show_generic_page(page, "OVOS Date-Time Skill", data)



def handle_session_set(namespace, session_data, component_map, page):
    if namespace in component_map:
        handler = component_map[namespace].get("session_set")
        if handler:
            handler(session_data, page)

def handle_events_triggered(event_name, parameters, component_map, page):
    # General event handlers can be added here
    if event_name == "page_gained_focus":
        focus_page = parameters.get("number", 0)
        print(f"Focus shifted to page {focus_page}")
        # Add logic here to handle the focused page
    # Add more event handlers as needed

def handle_list_insert(data, component_map, page):
    namespace = data.get("namespace")
    values = data.get("values", [])
    if namespace in component_map:
        handler = component_map[namespace].get("list_insert")
        if handler:
            handler(values, page)

# Listen to GUI WebSocket
def listen_to_ovos_gui(ws, page, component_map):
    try:
        while True:
            response = ws.recv()  # Receive messages from the WebSocket
            if response:
                data = json.loads(response)
                print("Received message:", data)
                process_gui_message(data, page, component_map)
    except Exception as e:
        print(f"Error receiving message: {e}")

# Send an event to OVOS-GUI
def send_focus_event(ws, namespace, page_index):
    if ws:
        message = {
            "type": "mycroft.events.triggered",
            "namespace": namespace,
            "event_name": "page_gained_focus",
            "data": {"number": page_index}
        }
        ws.send(json.dumps(message))

# Function to show a generic page
def show_generic_page(page, title, message, extra_data=None):
    """Displays a generic page with dynamic data."""
    data_controls = []
    if extra_data:
        for key, value in extra_data.items():
            data_controls.append(ft.Text(f"{key}: {value}", size=18))

    new_view = ft.View(
        f"/{title.lower()}",
        controls=[
            ft.Text(message, size=50, weight=ft.FontWeight.BOLD),
            ft.Text(f"{title} Skill", size=20),
            ft.Column(data_controls, spacing=10),  # Dynamically generated content
            ft.ElevatedButton("Back to Home", on_click=lambda _: navigate_to_home(page)),
        ],
    )
    page.views.clear()
    page.views.append(new_view)
    page.update()

# Function for the Hello World page
def show_hello_world_page(page, message):
    hello_world_view = ft.View(
        "/hello_world",  # Make sure to pass the correct page name
        controls=[
            ft.Column(
                [
                    ft.Text("Hello World Skill", size=50, weight=ft.FontWeight.BOLD, color="blue"),
                    ft.Text(message, size=20, weight=ft.FontWeight.NORMAL),
                    ft.ElevatedButton(
                        "Back to Home",
                        on_click=lambda _: navigate_to_home(page),  # Back button to home
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ],
    )
    page.views.append(hello_world_view)  # Add the new view to the page
    page.update()  # Update the page to apply changes

# Function to navigate to home page
def navigate_to_home(page):
    # Function to reload the home screen
    update_home_page(page)

def update_home_page(page):
    time_text = ft.Text(size=150, color="white", weight=ft.FontWeight.BOLD)

    # Background settings
    background_container = ft.Container(
        expand=True,
        image_src=WALLPAPER,
        image_fit=ft.ImageFit.COVER,
    )

    overlay = ft.Container(
        content=ft.Column(
            [
                time_text,
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
            ft.Stack([background_container, overlay], expand=True),
        ],
    )
    page.views.clear()  # Remove old views
    page.views.append(home_view)  # Add the home view
    page.update()  # Update the page

    # Update time
    def update_time():
        while True:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            time_text.value = current_time
            page.update()
            time.sleep(1)

    threading.Thread(target=update_time, daemon=True).start()

# Main Flet app setup
def main(page):
    page.title = "OVOS Homescreen"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    update_home_page(page)

    # Connect to WebSocket and listen for messages
    ws = connect_to_ovos_gui()
    if ws:
        threading.Thread(target=listen_to_ovos_gui, args=(ws, page, {}), daemon=True).start()

# Start the Flet app
ft.app(target=main)
