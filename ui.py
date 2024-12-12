import pygame

class UIManager:
    def __init__(self, screen, font, color):
        self.screen = screen
        self.font = font
        self.color = color
        self.text_elements = {}
        self.button_elements = {}
        self.console = []
        self.y_padding = 0

    def add_text(self, name, text, x, y):
        """Add a text element to the UI."""
        self.text_elements[name] = {"text": text, "pos": (x, y + self.y_padding)}
        self.y_padding += y

    def update_text(self, name, new_text):
        """Update the text of an existing element."""
        if name in self.text_elements:
            self.text_elements[name]["text"] = new_text

    def add_button(self, name, button):
        self.button_elements[name] = button

    def add_to_console(self, text):
        self.console.append(text)

    def handle_event(self, event):
        for button in self.button_elements.values():
            button.handle_event(event)

    def need_target(self) -> bool:
        for button in self.button_elements.values():
            if not button.act_on_click and button.clicked:
                return True
        return False
    
    def act_with_target(self):
        for button in self.button_elements.values():
            if not button.act_on_click and button.clicked:
                button.action()
                button.clicked = False
                return 

    def draw(self):
        """Render all UI elements to the screen."""
        for element in self.text_elements.values():
            text_surface = self.font.render(element["text"], True, self.color)
            self.screen.blit(text_surface, element["pos"])

        for button in self.button_elements.values():
            button.draw(self.screen)

        for text in self.console:
            text_surface = self.font.render(text, True, self.color)
            self.screen.blit(text_surface, (400, 400))