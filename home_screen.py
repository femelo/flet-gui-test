from __future__ import annotations
import shutil
import os
from typing import Any, Optional, Dict
from flet import (
    Text,
    FontWeight,
    Container,
    ImageFit,
    Column,
    CrossAxisAlignment,
    MainAxisAlignment,
    alignment,
    Stack,
    View,
)


# Background image
WALLPAPER = "https://cdn.pixabay.com/photo/2016/06/02/02/33/triangles-1430105_1280.png"


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
        # Background settings
        self._background_container = Container(
            key="selected_wallpaper",
            expand=True,
            image_src=self._session_data["selected_wallpaper"],
            image_fit=ImageFit.COVER,
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
                Stack([self._background_container, self._overlay], expand=True),
            ],
        )

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
