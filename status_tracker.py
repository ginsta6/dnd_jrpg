from character import Character

class StatusTracker():
    def __init__(self, character: Character):
        self.character = character
        self.current_hp = character.hp
        self.conditions = set()