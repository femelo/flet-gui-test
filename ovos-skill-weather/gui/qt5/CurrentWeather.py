import flet as ft
import os  # Voor dynamisch padbeheer

def get_view(page, message_store):
    # Specificeer het namespace voor de weersinformatie
    namespace = "skill-ovos-weather.openvoiceos"
    
    # Controleer of het namespace in message_store zit
    if namespace in message_store:
        # Verkrijg de weersinformatie uit de message_store
        weather_data = message_store[namespace]
        
        # Haal de relevante gegevens op uit het bericht
        weather_code = weather_data.get('weatherCode', 'N/A')
        current_temperature = weather_data.get('currentTemperature', 'N/A')
        high_temperature = weather_data.get('highTemperature', 'N/A')
        low_temperature = weather_data.get('lowTemperature', 'N/A')
        chance_of_precipitation = weather_data.get('chanceOfPrecipitation', 'N/A')
        wind_speed = weather_data.get('windSpeed', 'N/A')
        humidity = weather_data.get('humidity', 'N/A')
        weather_location = weather_data.get('weatherLocation', 'Unknown Location')
        weather_condition = weather_data.get('weatherCondition', 'No Condition Image')

    else:
        # Gebruik standaardwaarden als er geen gegevens beschikbaar zijn
        weather_code = "N/A"
        current_temperature = "N/A"
        high_temperature = "N/A"
        low_temperature = "N/A"
        chance_of_precipitation = "N/A"
        wind_speed = "N/A"
        humidity = "N/A"
        weather_location = "Unknown Location"
        weather_condition = "No Condition Image"

    # Dynamisch pad naar de Lottie-animatie
    script_dir = os.path.dirname(__file__)  # Huidige scriptlocatie
    lottie_path = os.path.join(script_dir, "weather.json")  # Pad naar de animatie

    # Hoofd lay-out
    def main_layout():
        # Datum en locatie
        header = ft.Column(
            [
                ft.Text("Huidig Weer", size=24, weight=ft.FontWeight.BOLD, color="white"),
                ft.Text(weather_location, size=18, color="white"),
            ],
            spacing=5,
        )

        # Lottie animatie voor weersymbool
        weather_animation = ft.Lottie(
            src=lottie_path,  # Lokale pad naar weer.json
            width=150,
            height=150,
            animate=True,
            fit=ft.ImageFit.CONTAIN,
        )

        # Hoofdtemperatuur
        current_temp = ft.Text(
            f"{current_temperature}°", size=80, weight=ft.FontWeight.BOLD, color="black"
        )

        # Max en Min temperatuur
        min_max_temp = ft.Row(
            [
                ft.Column(
                    [
                        ft.Icon(ft.icons.ARROW_UPWARD, size=24, color="black"),
                        ft.Text(
                            f"{high_temperature}°",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color="black",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Column(
                    [
                        ft.Icon(ft.icons.ARROW_DOWNWARD, size=24, color="black"),
                        ft.Text(
                            f"{low_temperature}°",
                            size=20,
                            weight=ft.FontWeight.NORMAL,
                            color="black",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Extra informatie (Neerslag, Wind, Luchtvochtigheid)
        extra_info = ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.icons.WATER_DROP, size=24, color="white"),
                        ft.Text(f"{chance_of_precipitation}%", size=20, color="white"),
                    ],
                    spacing=10,
                ),
                ft.Row(
                    [
                        ft.Icon(ft.icons.AIR, size=24, color="white"),
                        ft.Text(f"{wind_speed} km/h", size=20, color="white"),
                    ],
                    spacing=10,
                ),
                ft.Row(
                    [
                        ft.Icon(ft.icons.WAVES, size=24, color="white"),
                        ft.Text(f"{humidity}%", size=20, color="white"),
                    ],
                    spacing=10,
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        )

        # Samenstellen van de lay-out
        return ft.Container(
            content=ft.Column(
                [
                    header,
                    ft.Row(
                        [
                            weather_animation,
                            ft.Column(
                                [current_temp, min_max_temp],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            extra_info,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                spacing=20,
            ),
            bgcolor="#87CEEB",  # Lichtblauwe achtergrondkleur
            padding=20,
            expand=True,
        )

    # Retourneer de view
    return ft.View(
        "/weather",
        controls=[
            ft.AppBar(title=ft.Text("Weer App"), bgcolor=ft.colors.SURFACE_VARIANT),
            main_layout(),
            ft.ElevatedButton("Terug naar start", on_click=lambda _: page.go("/")),
        ],
    )


# Voorbeeld van hoe je de app runt met message_store
def main(page: ft.Page):
    message_store = {
        "skill-ovos-weather.openvoiceos": {
            "weatherCode": "clear-day",
            "currentTemperature": 7.9,
            "highTemperature": 10.8,
            "lowTemperature": 5.8,
            "chanceOfPrecipitation": 14,
            "windSpeed": 12.1,
            "humidity": 78,
            "weatherLocation": "Haarlem, The Netherlands",
            "weatherCondition": "Clear",
        }
    }
    page.views.append(get_view(page, message_store))



