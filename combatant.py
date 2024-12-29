import pygame
from character import Character
from status_tracker import StatusTracker
from random import randint
from console import Console

class Combatant(pygame.sprite.Sprite):
    def __init__(self, x, y, character: Character, status_tracker: StatusTracker, image_path: str, console: Console):
        super().__init__()
        self.image = pygame.Surface((100,100))
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100,100))
        self.rect = self.image.get_rect(topleft=(x,y))

        self.character = character
        self.status_tracker = status_tracker
        self.console = console
        self.bob = True


    def update(self):
        if self.bob:
            self.rect.y += 5
            self.bob = False
        else:
            self.rect.y -= 5
            self.bob = True


    def apply_condition(self, condition):
        self.status_tracker.apply_condition(condition)

    def remove_condition(self, condition):
        self.status_tracker.remove_condition(condition)

    def get_status(self):
        return self.status_tracker.show_status()
    
    def use_action(self, action_id, target):
        self.character.use_action(action_id, target, self.status_tracker.attributes)

    def use_random_action(self, target):
        action_id = randint(0, self.character.actions.__len__() - 1)
        self.character.use_action(action_id, target, self.status_tracker.attributes)

    def handle_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return self.character._name

    def __str__(self):
        return f"{self.character._name} - {self.character._type} - HP: {self.status_tracker.current_hp} - AC: {self.character._ac}"
