from __future__ import annotations
from typing import Any, Optional, Dict
from flet import (
    View,
    Column,
    Text,
    FontWeight,
    ElevatedButton,
    MainAxisAlignment,
    CrossAxisAlignment,
)


class HelloWorldPage:
    _is_page: bool = True

    def __init__(
        self: HelloWorldPage,
        session_data: Optional[Dict[str, Any]] = None,
    ):
        self._session_data: Dict[str, Any] = {
            "title": "Flet Hello World Skill",
            "text": "Hello world!",
        }
        if session_data:
            self._session_data.update(session_data)
        self._title: Text = Text(
            self._session_data["title"],
            key="title",
            size=50,
            weight=FontWeight.BOLD,
            color="blue"
        )
        self._text: Text = Text(
            self._session_data["text"],
            key="text",
            size=20,
            weight=FontWeight.NORMAL
        )
        self._button: ElevatedButton = ElevatedButton(
            "Back to Home",
            on_click=None,  # Back button to home
        )
        self._view: View = View(
            "/hello_world",  # Make sure to pass the correct page name
            controls=[
                Column(
                    [
                        self._title,
                        self._text,
                        self._button,
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
            ],
        )

    @property
    def page(self: HelloWorldPage) -> View:
        return self._view

    def update_session_data(
        self: HelloWorldPage,
        session_data: Dict[str, Any],
        renderer: Any
    ) -> None:
        self._session_data.update(session_data)
        for key, value in self._session_data.items():
            renderer.update_attributes(
                route="/hello_world",
                key=key,
                attributes={"value": value},
            )

    def update(self: HelloWorldPage, renderer: Any) -> None:
        renderer.update()

    def set(self: HelloWorldPage, renderer: Any) -> None:
        self._button.on_click = lambda _: renderer.close()
