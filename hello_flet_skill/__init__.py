from ovos_workshop.skills import OVOSSkill
from ovos_workshop.decorators import intent_handler

class HelloWorldSkill(OVOSSkill):
    def __init__(self):
        super().__init__()

    @intent_handler("flet.intent")
    def handle_hello_world(self, message):
        # The message you want to display and speak
        message_text = "Hello world"
        
        # Set the data in the GUI session
        self.gui['message_text'] = message_text  # Place the message in sessionData

        # Call the generic page with the correct data (data contains the message)
        self.gui.show_page("hallo_flet")  # The page will be loaded with sessionData available

        # Optionally: Speak the message as a confirmation
        self.speak(message_text)
