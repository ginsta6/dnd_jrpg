import pygame

class UIManager:
    def __init__(self, screen, font, color):
        self.screen = screen
        self.font = font
        self.color = color
        self.elements = {}

    def add_text(self, name, text, x, y):
        """Add a text element to the UI."""
        self.elements[name] = {"text": text, "pos": (x, y)}

    def update_text(self, name, new_text):
        """Update the text of an existing element."""
        if name in self.elements:
            self.elements[name]["text"] = new_text

    def draw(self):
        """Render all UI elements to the screen."""
        for element in self.elements.values():
            text_surface = self.font.render(element["text"], True, self.color)
            self.screen.blit(text_surface, element["pos"])