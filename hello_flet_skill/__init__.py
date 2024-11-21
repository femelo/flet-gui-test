from ovos_workshop.skills import OVOSSkill
from ovos_workshop.decorators import intent_handler

class HelloWorldSkill(OVOSSkill):
    def __init__(self):
        super().__init__()

    @intent_handler("flet.intent")
    def handle_hello_world(self, message):
        message_text = "Hello world, this is a new GUI"
        
        self.gui.show_page("hello_world", message_text)  # Dit genereert een WebSocket-bericht

        self.speak(message_text)
