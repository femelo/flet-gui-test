from __future__ import annotations
import shutil
import os
from typing import Any, Optional, Dict
from flet import (
    Text,
    FontWeight,
    Container,
    Image,
    ImageFit,
    Column,
    CrossAxisAlignment,
    MainAxisAlignment,
    Row,
    alignment,
    Stack,
    View,
)

# Background image
WALLPAPER = "https://cdn.pixabay.com/photo/2016/06/02/02/33/triangles-1430105_1280.png"

# Weather icon mapping
WEATHER_ICONS = {
    0: "icons/sun.svg",
    1: "icons/partial_clouds.svg",
    2: "icons/clouds.svg",
    3: "icons/rain.svg",
    4: "icons/rain.svg",
    5: "icons/storm.svg",
    6: "icons/snow.svg",
    7: "icons/fog.svg",
}


class HomeScreen:
    _is_page: bool = True  # required class attribute for correct loading

    def __init__(
        self: HomeScreen,
        session_data: Optional[Dict[str, Any]],
    ):
        self._session_data: Dict[str, Any] = {
            "notification": {},
            "notification_model": [],
            "system_connectivity": "offline",
            "persistent_menu_hint": False,
            "applications_model": [
                {   "name": "OCP",
                    "thumbnail": "/home/flavio/.cache/ovos_gui/ovos.common_play/OCP.png",
                    "action": "ovos.common_play.OCP.homescreen.app",
                },
            ],
            "apps_enabled": True,
            "time_string": "",
            "date_string": "",
            "weekday_string": "",
            "day_string": "",
            "month_string": "",
            "year_string": "",
            "skill_info_enabled": False,
            "skill_info_prefix": False,
            "rtl_mode": 0,
            "dateFormat": "MDY",
            "wallpaper_path": "",
            "selected_wallpaper": "default.jpg",
            "weather_code": None,
            "weather_temp": None,
        }
        if session_data:
            self._session_data.update(session_data)
        self._element_keys = {
            "time_string": "time_string",
            "weekday_string": "full_date_string",
            "day_string": "full_date_string",
            "month_string": "full_date_string",
            "year_string": "full_date_string",
            "selected_wallpaper": "selected_wallpaper",
        }
        self._time_text: Text = Text(
            key="time_string",
            size=200,
            color="white",
            weight=FontWeight.BOLD
        )
        self._full_date_text: Text = Text(
            key="full_date_string",
            size=100,
            color="white",
            weight=FontWeight.BOLD
        )
        self._weather_icon: Image = Image(
            src=self._get_weather_icon_src(),
            width=100,
            height=100,
            fit=ImageFit.CONTAIN,
        )
        self._weather_temp_text: Text = Text(
            self._format_weather_temp(),
            size=50,
            color="white",
            weight=FontWeight.BOLD,
        )

        # Background settings
        self._background_container = Container(
            key="selected_wallpaper",
            expand=True,
            image_src=self._session_data["selected_wallpaper"],
            image_fit=ImageFit.COVER,
        )
        self._weather_container = Container(
            content=Row(
                [
                    self._weather_icon,
                    self._weather_temp_text,
                ],
                alignment="end",
                vertical_alignment="center",
                spacing=10,
            ),
            padding=20,
            alignment=alignment.top_right,
        )
        self._overlay = Container(
            content=Column(
                [
                    self._time_text,
                    self._full_date_text,
                ],
                alignment=MainAxisAlignment.END,
                horizontal_alignment=CrossAxisAlignment.START,
                spacing=10,
            ),
            padding=20,
        )
        self._view = View(
            "/home",
            controls=[
                Stack(
                    [
                        self._background_container,
                        self._weather_container,
                        self._overlay,
                    ],
                    expand=True,
                ),
            ],
        )

    def _get_weather_icon_src(self) -> str:
        """Returns the local file path for the weather icon."""
        weather_code = self._session_data.get("weather_code")
        if weather_code is not None and weather_code in WEATHER_ICONS:
            return WEATHER_ICONS[weather_code]
        return "icons/default.svg"  # Fallback icon if weather_code is missing or invalid

    def _format_weather_temp(self) -> str:
        """Formats the temperature with °C."""
        weather_temp = self._session_data.get("weather_temp")
        if weather_temp is not None:
            return f"{weather_temp}°C"
        return ""

    @property
    def page(self: HomeScreen) -> View:
        return self._view

    @property
    def full_date(self: HomeScreen) -> str:
        weekday = self._session_data["weekday_string"][:3].title()
        month = self._session_data["month_string"].title()
        day = self._session_data["day_string"]
        year = self._session_data["year_string"]
        return f"{weekday} {month} {day}, {year}"

    @property
    def wallpaper_uri(self: HomeScreen) -> str:
        wallpaper_path = self._session_data["wallpaper_path"]
        selected_wallpaper = self._session_data["selected_wallpaper"]
        if wallpaper_path:
            # Hack to workaround the way Flet serves figures
            shutil.copy(
                os.path.join(wallpaper_path, selected_wallpaper),
                "assets/",
            )
        return selected_wallpaper

    def update_session_data(
        self: HomeScreen,
        session_data: Dict[str, Any],
        renderer: Any
    ) -> None:
        self._session_data.update(session_data)

        # Update weather icon and temperature
        self._weather_icon.src = self._get_weather_icon_src()
        self._weather_temp_text.value = self._format_weather_temp()

        for key, value in session_data.items():
            if key not in self._element_keys:
                continue
            element_key = self._element_keys[key]
            if element_key == "full_date_string":
                attr_name = "value"
                attr_value = self.full_date
                self._full_date_text.value = attr_value
            elif element_key == "selected_wallpaper":
                attr_name = "image_src"
                attr_value = self.wallpaper_uri
                self._background_container.image_src = attr_value
            else:
                attr_name = "value"
                attr_value = value
                self._time_text.value = attr_value
            print(f"Updating {element_key} with {attr_name}={attr_value} in /home.")
            renderer.update_attributes(
                route="/home",
                key=element_key,
                attributes={attr_name: attr_value},
            )

    def set(self: HomeScreen, renderer: Any) -> None:
        # No callback to set
        pass
