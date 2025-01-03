class TurnManager:
    def __init__(self):
        self.turn_queue: list[str] = []
        self.current_turn: int = 0
        self.player_names: list[str] = ["Berserker", "Acolyte"]

    def add_to_queue(self, item: str):
        """Add an item to the turn queue."""
        if isinstance(item, list):
            self.turn_queue.extend(item)
        else:
            self.turn_queue.append(item)

    def remove_from_queue(self, item: str):
        """Remove an item from the turn queue."""
        try:
            self.turn_queue.remove(item)
            if item in self.player_names:
                self.player_names.remove(item)
        except ValueError:
            print("Combatant does not exist in turn queue")

    def take_turn(self):
        """Return the next combatant in the turn queue."""
        ans = self.turn_queue[self.current_turn]
        self.current_turn = (self.current_turn + 1) % len(self.turn_queue)
        return ans

    def is_player_turn(self):
        """Return True if it is a player's turn, False otherwise."""
        current_combatant = self.turn_queue[self.current_turn]
        if current_combatant in self.player_names:
            return True
        else:
            return False

    def __str__(self):
        return f"Current turn: {self.turn_queue[self.current_turn]}"
