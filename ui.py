import pygame

class UIManager:
    def __init__(self, screen, color):
        self.screen = screen
        self.font = pygame.font.Font("./assets/PixelatedEleganceRegular.ttf", 20)
        self.cfont = pygame.font.Font("./assets/PixelatedEleganceRegular.ttf", 15)
        self.color = color
        self.text_elements = {}
        self.button_elements = {}
        self.console = []
        self.cwidth = 900
        self.cheight = 150
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


    def update_console(self):
        textbox_surface = pygame.Surface((self.cwidth, len(self.console) * 25))
        textbox_surface.fill((0,0,0))
        for i, line in enumerate(self.console):
            text_surface = self.cfont.render(line, True, self.color)
            textbox_surface.blit(text_surface, (10,10 + i * 25))
        return textbox_surface