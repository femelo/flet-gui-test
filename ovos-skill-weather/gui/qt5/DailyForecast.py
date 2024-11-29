import flet as ft

def get_view(page, message_store):
    # Specificeer het namespace voor de dagelijkse weersvoorspelling
    namespace = "skill-ovos-weather.openvoiceos"
    
    # Controleer of het namespace in message_store zit
    if namespace in message_store:
        # Verkrijg de dagelijkse weersvoorspelling uit de message_store
        daily_forecast = message_store[namespace].get('forecast', {}).get('all', [])
        
        # Als er geen voorspellingen zijn, geef dan een standaard bericht
        if not daily_forecast:
            forecast_display = "Geen dagelijkse voorspelling ontvangen."
        else:
            forecast_display = ""
            # Loop door de dagen in de forecast en voeg ze toe aan de display string
            for forecast in daily_forecast:
                date = forecast.get('date', 'N/A')
                high_temp = forecast.get('highTemperature', 'N/A')
                low_temp = forecast.get('lowTemperature', 'N/A')
                weather_condition = forecast.get('weatherCondition', 'N/A')
                
                forecast_display += (
                    f"Date: {date}\n"
                    f"High Temperature: {high_temp}°C\n"
                    f"Low Temperature: {low_temp}°C\n"
                    f"Condition: {weather_condition}\n\n"
                )
    else:
        forecast_display = "Geen dagelijkse voorspelling ontvangen."

    # Maak de view met de opgehaalde dagelijkse weersvoorspelling
    return ft.View(
        "/DailyForecast",
        [
            ft.AppBar(title=ft.Text("Daily Forecast"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Text(value=forecast_display),  # Toon de dagelijkse weersvoorspelling
            ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
        ],
    )
