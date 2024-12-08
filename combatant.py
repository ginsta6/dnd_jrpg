import pygame
from character import Character
from status_tracker import StatusTracker

class Combatant(pygame.sprite.Sprite):
    def __init__(self, x, y, character: Character, status_tracker: StatusTracker):
        super().__init__()
        self.image = pygame.Surface((50,50))
        self.image.fill("Blue")
        self.rect = self.image.get_rect(topleft=(x,y))
        self.character = character
        self.status_tracker = status_tracker


    def update(self):
        ...

    def __str__(self):
        return self.character.__str__()