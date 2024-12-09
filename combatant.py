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

    def apply_condition(self, condition):
        self.status_tracker.apply_condition(condition)

    def remove_condition(self, condition):
        self.status_tracker.remove_condition(condition)

    def get_status(self):
        return self.status_tracker.show_status()
    
    def use_action(self, action_id, target):
        self.character.use_action(action_id, target, self.status_tracker.attributes)

    def __str__(self):
        return f"{self.character._name} - {self.character._type} - HP: {self.status_tracker.current_hp} - AC: {self.character._ac}"
