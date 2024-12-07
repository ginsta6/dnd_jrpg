import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, text_color, button_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.action = action

    def draw(self, screen):
        # Draw the button's background
        pygame.draw.rect(screen, self.button_color, self.rect)
        
        # Render the text on top of the button
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_hovered(self, mouse_pos):
        """Check if the mouse is hovering over the button."""
        return self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        """Handle click event on the button."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if self.is_hovered(pygame.mouse.get_pos()):
                if self.action:
                    self.action()