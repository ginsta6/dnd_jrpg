from character import Character
from rules import Ruleset

class StatusTracker():
    def __init__(self, character: Character):
        self.character = character
        self.max_hp = character.hp
        self.current_hp = character.hp
        self.conditions = set()
        self.attributes = Ruleset.default_attributes.copy()

    def damage(self, amount, type=""):
        self.current_hp = max(0, self.current_hp - amount)
        return self.current_hp > 0
    
    def heal(self, amount):
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def apply_condition(self, condition):
        if condition not in Ruleset.conditions:
            print(f"ERROR: {condition} is not a valid condition.")
            return

        print(f"{self.character._name} is now {condition}")
        self.conditions.add(condition)
        self._update_effects()

    def remove_condition(self, condition):
        if condition in self.conditions:
            print(f"{self.character._name} is no longer {condition}")
            self.conditions.remove(condition)
            self._update_effects()

    def _update_effects(self):
        self.attributes = Ruleset.default_attributes.copy()

        for condition in self.conditions:
            effects = Ruleset.conditions[condition]
            for attr, value in effects.items():
                self.attributes[attr] = value

    def show_status(self):
        status = (
            f"\n{self.character._name}'s Status:\n"
            f"Conditions: {', '.join(self.conditions) or 'None'}\n"
            f"Attributes:\n"
        )

        attributes = "\n".join(f"  {key}: {value}" for key, value in self.attributes.items())
        status += attributes

        return status
