from __future__ import annotations
# import os
# from typing import Optional
# from ovos_bus_client import MessageBusClient
# from ovos_bus_client.apis.gui import GUIInterface
from ovos_workshop.skills import OVOSSkill
from ovos_workshop.decorators import intent_handler

class HelloWorldSkill(OVOSSkill):
    def __init__(
        self: HelloWorldSkill,
        skill_id: str = "skill-flet-hello-world",
    ):
        super().__init__(skill_id=skill_id)

    @intent_handler("flet.intent")
    def handle_hello_world(self: HelloWorldSkill):
        text = "Hello world, this is a new GUI"
        
        self.gui["title"] = "Flet-based Hello World"
        self.gui["text"] = text
        self.gui.show_page("hello_world")  # Dit genereert een WebSocket-bericht

        self.speak(text)

