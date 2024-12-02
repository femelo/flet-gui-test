from __future__ import annotations
import os
from typing import Optional
from ovos_bus_client import MessageBusClient
from ovos_bus_client.apis.gui import GUIInterface
from ovos_workshop.skills import OVOSSkill
from ovos_workshop.decorators import intent_handler

class HelloWorldSkill(OVOSSkill):
    def __init__(
        self: HelloWorldSkill,
        skill_id: str = "skill-flet-hello-world",
        bus: Optional[MessageBusClient] = None,
    ):
        super().__init__(
            gui=GUIInterface(
                skill_id=skill_id,
                bus=bus,
                # TODO: this should be detected automatically.
                # There should not be the need for instatiating
                # a GUIInterface here.
                ui_directories={
                    "py-flet": os.path.join(
                        os.path.dirname(__file__),
                        "gui",
                        "py-flet"
                    )
                },
            ),
            skill_id=skill_id,
            bus=bus,
        )

    @intent_handler("flet.intent")
    def handle_hello_world(self: HelloWorldSkill):
        text = "Hello world, this is a new GUI"
        
        self.gui["title"] = "Flet-based Hello World"
        self.gui["text"] = text
        self.gui.show_page("hello_world")  # Dit genereert een WebSocket-bericht

        self.speak(text)
