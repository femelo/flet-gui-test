import flet as ft

def get_view(page, message_store):
    # Specificeer het namespace voor de uurlijkse weersvoorspelling
    namespace = "skill-ovos-weather.openvoiceos"
    
    # Controleer of het namespace in message_store zit
    if namespace in message_store:
        # Verkrijg de uurlijkse weersvoorspelling uit de message_store
        hourly_forecast = message_store[namespace].get('hourlyForecast', {}).get('hours', [])
        
        # Als er geen uren zijn, geef dan een standaard bericht
        if not hourly_forecast:
            forecast_display = "Geen uurlijkse voorspelling ontvangen."
        else:
            forecast_display = ""
            # Loop door de uren in de forecast en voeg ze toe aan de display string
            for forecast in hourly_forecast:
                time = forecast.get('time', 'N/A')
                precipitation = forecast.get('precipitation', 'N/A')
                temperature = forecast.get('temperature', 'N/A')
                weather_condition = forecast.get('weatherCondition', 'N/A')
                
                forecast_display += (
                    f"Time: {time}\n"
                    f"Temperature: {temperature}°C\n"
                    f"Precipitation: {precipitation}%\n"
                    f"Condition: {weather_condition}\n\n"
                )
    else:
        forecast_display = "Geen uurlijkse voorspelling ontvangen."

    # Maak de view met de opgehaalde uurlijkse weersvoorspelling
    return ft.View(
        "/HourlyForecast",
        [
            ft.AppBar(title=ft.Text("Hourly Forecast"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Text(value=forecast_display),  # Toon de uurlijkse weersvoorspelling
            ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
        ],
    )
