from characters.character import Character
from utils.rules import Ruleset


class StatusTracker:
    def __init__(self, character: Character):
        self.character = character
        self.max_hp = character.hp
        self.current_hp = character.hp
        self.conditions = set()
        self.attributes = Ruleset.default_attributes.copy()

    def damage(self, amount, type=""):
        """Apply damage to the character."""
        self.current_hp = max(0, self.current_hp - amount)
        return self.current_hp > 0

    def heal(self, amount):
        """Heal the character."""
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def apply_condition(self, condition):
        """Apply the specified condition to the character."""
        if condition not in Ruleset.conditions:
            print(f"ERROR: {condition} is not a valid condition.")
            return

        print(f"{self.character._name} is now {condition}")
        self.conditions.add(condition)
        self._update_effects()

    def remove_condition(self, condition):
        """Remove the specified condition from the character."""
        if condition in self.conditions:
            print(f"{self.character._name} is no longer {condition}")
            self.conditions.remove(condition)
            self._update_effects()

    def _update_effects(self):
        """Update the character's attributes based on their conditions"""
        self.attributes = Ruleset.default_attributes.copy()

        for condition in self.conditions:
            effects = Ruleset.conditions[condition]
            for attr, value in effects.items():
                self.attributes[attr] = value

    def show_status(self):
        """Return a string representation of the character's status."""
        status = (
            f"\n{self.character._name}'s Status:\n"
            f"Conditions: {', '.join(self.conditions) or 'None'}\n"
            f"Attributes:\n"
        )

        attributes = "\n".join(
            f"  {key}: {value}" for key, value in self.attributes.items()
        )
        status += attributes

        return status

    def get_status(self):
        """Return the current status conditions of the combatant."""
        return ", ".join(self.conditions) or "Clear"

    def is_dead(self):
        """Return whether the character is dead."""
        return self.current_hp <= 0
