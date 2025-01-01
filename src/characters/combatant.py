import pygame
from characters.character import Character
from characters.status_tracker import StatusTracker
from random import shuffle
from utils.console import Console


class Combatant(pygame.sprite.Sprite):
    def __init__(
        self,
        x,
        y,
        character: Character,
        status_tracker: StatusTracker,
        image_path: str,
        console: Console,
    ):
        super().__init__()
        self.image = pygame.Surface((100, 100))
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))

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
        """Apply the specified condition to the combatant."""
        if condition not in self.character.condition_immunities:
            self.status_tracker.apply_condition(condition)
            self.console.log(f"{self.character._name} is now {condition}.")
        else:
            self.console.log(f"{self.character._name} is immune to {condition}.")

    def remove_condition(self, condition):
        """Remove the specified condition from the combatant."""
        self.status_tracker.remove_condition(condition)

    def get_status(self):
        """Return the current status of the combatant."""
        return self.status_tracker.show_status()

    def use_action(self, action_id, target):
        """Use the specified action"""
        self.character.use_action(action_id, target, self.status_tracker.attributes)

    def use_random_action(self, target):
        """Use a random action from the character's list of actions."""
        action_indices = list(range(len(self.character.actions)))
        shuffle(action_indices)  # Randomize the order of actions

        for action_id in action_indices:
            if not self.character.check_action(action_id):
                self.character.use_action(
                    action_id, target, self.status_tracker.attributes
                )
                return

        # If no valid action is found
        self.status_tracker.attributes.console.log("No valid actions available.")

    def handle_click(self, mouse_pos):
        """Handle a click event on the combatant"""
        if self.rect.collidepoint(mouse_pos):
            return self.character._name

    def __str__(self):
        return f"{self.character._name} - {self.character._type} - HP: {self.status_tracker.current_hp} - AC: {self.character._ac} - Conditions: {self.status_tracker.get_status()}"
