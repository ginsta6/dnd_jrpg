from dice import Dice

class Action():
    def __init__(self, data: dict):
        self._name = data.get("name")
        self._description = data.get("desc")
        self._usage = data.get("usage")
        self._bonus = data.get("attack_bonus")
        self._dc = data.get("dc") # maybe make a DC class / interface?
        self._damage = data.get("damage") # maybe make a class or struct or something. define the parameters somehow. Action can have multiple damage types
        self._options = data.get("options")

    
    def use_action(self, target, advantage: int):
        if self._usage:
            # Special use algorithm (saving throw for target)
            ...
        elif self._name == "Multiattack":
            # multiattack alogrithm
            ...
        elif self._damage:
            # regular attack algorithm
            self._regular_attack(target, advantage)

    def _regular_attack(self, target, advantage: int):
        if advantage > 0:
            to_hit = max(Dice.roll_dice(), Dice.roll_dice()) + self._bonus
        elif advantage < 0:
            to_hit = min(Dice.roll_dice(), Dice.roll_dice()) + self._bonus
        else:
            to_hit = Dice.roll_dice() + self._bonus
            
        if to_hit >= target.character.ac:
            damage = Dice.roll_dice(self._damage[0]["damage_dice"])
            target.status_tracker.damage(damage)

    def __repr__(self):
        return (
            f"Action(name={self._name!r}, description={self._description!r}, "
            f"usage={self._usage!r}, bonus={self._bonus!r}, "
            f"dc={self._dc!r}, damage={self._damage!r}, options={self._options!r})\n"
        )