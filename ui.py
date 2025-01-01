import pygame
from console import Console


class UIManager:
    def __init__(self, screen, color):
        self.screen = screen
        self.font = pygame.font.Font("./assets/PixelatedEleganceRegular.ttf", 20)
        self.color = color
        self.text_elements = {}
        self.button_elements = {}
        self.y_padding = 0

        self._console = Console()
        self.cfont = pygame.font.Font("./assets/PixelatedEleganceRegular.ttf", 15)
        self.cwidth = 900
        self.cheight = 150

    def add_text(self, name, text, x, y):
        """Add a text element to the UI."""
        if name in self.text_elements:
            self.update_text(name, text)
        else:
            self.text_elements[name] = {"text": text, "pos": (x, y + self.y_padding)}
            self.y_padding += y

    def remove_text(self, name):
        """Remove a text element from the UI."""
        if name in self.text_elements:
            del self.text_elements[name]

    def update_text(self, name, new_text):
        """Update the text of an existing element."""
        if name in self.text_elements:
            self.text_elements[name]["text"] = new_text

    def add_button(self, name, button):
        """Add a button element to the UI."""
        self.button_elements[name] = button

    def handle_event(self, event):
        """Handle events for all UI elements."""
        for button in self.button_elements.values():
            button.handle_event(event)

    def need_target(self) -> bool:
        """Check if any buttons need a target."""
        for button in self.button_elements.values():
            if not button.act_on_click and button.clicked:
                return True
        return False

    def act_with_target(self):
        """Act on a button that requires a target."""
        for button in self.button_elements.values():
            if not button.act_on_click and button.clicked:
                button.clicked = False
                return button.action()

    def draw(self):
        """Render all UI elements to the screen."""
        for element in self.text_elements.values():
            text_surface = self.font.render(element["text"], True, self.color)
            self.screen.blit(text_surface, element["pos"])

        for button in self.button_elements.values():
            button.draw(self.screen)

    def update_console(self):
        """Update the console with the latest messages."""
        textbox_surface = pygame.Surface(
            (self.cwidth, len(self._console.get_messages()) * 25)
        )
        textbox_surface.fill((0, 0, 0))
        for i, line in enumerate(self._console.get_messages()):
            text_surface = self.cfont.render(line, True, self.color)
            textbox_surface.blit(text_surface, (10, 10 + i * 25))
        return textbox_surface

    @property
    def console(self):
        return self._console
