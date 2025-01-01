from dice import Dice
from console import Console
from rules import Ruleset
import re

class Action():
    def __init__(self, data: dict, console: Console):
        self._name = data.get("name")
        self._description = data.get("desc")
        self._usage = data.get("usage")
        self._bonus = data.get("attack_bonus")
        self._dc = data.get("dc") # maybe make a DC class / interface?
        self._damage = data.get("damage") # maybe make a class or struct or something. define the parameters somehow. Action can have multiple damage types
        self._options = data.get("options")
        self._console = console

    
    def use_action(self, target, advantage: int):
        if self._usage:
            # Special use algorithm (saving throw for target)
            self._special_attack(target)
        elif self._name == "Multiattack":
            # multiattack alogrithm
            ...
        elif self._damage:
            # regular attack algorithm
            self._regular_attack(target, advantage)

    def _special_attack(self, target):
        if self._usage == "recharge":
            # Check if the action can be used
            if Dice.roll_dice("1d6") >= 5:
                self._console.log(f"{self._name} recharged!")
            else:
                self._console.log(f"{self._name} failed to recharge.")
                return

        condition = self.get_condition()
        if condition[0]:
            self.attack_saving_throw_condition(target, condition)
        elif self._damage:
            print("doing a special attack")
            self.attack_saving_throw_damage(target)


    def _regular_attack(self, target, advantage: int):
        adjective = ""
        if advantage > 0:
            to_hit = max(Dice.roll_dice(), Dice.roll_dice()) + self._bonus
            adjective = "with advantage"
        elif advantage < 0:
            to_hit = min(Dice.roll_dice(), Dice.roll_dice()) + self._bonus
            adjective = "with disadvantage"
        else:
            to_hit = Dice.roll_dice() + self._bonus
            adjective = "straight"

        self._console.log(f"Rolled {adjective} and got: {to_hit}")
            
        if to_hit >= target.character.ac:
            damage = Dice.roll_dice(self._damage[0]["damage_dice"])
            target.status_tracker.damage(damage)

            condition = self.get_condition()
            if condition[0]: 
                self.attack_saving_throw_condition(target, condition)

            self._console.log(f"Rolled for damage and got: {damage}")
            
    def attack_saving_throw_condition(self, target, condition):
        condition_name, dc, saving_throw_skill = condition
        if dc:
            saving_throw = Dice.roll_dice("1d20") + target.character.get_skill(saving_throw_skill) // 2
            self._console.log(f"Rolled a {saving_throw_skill} saving throw and got: {saving_throw}")
            if saving_throw < int(dc):
                target.apply_condition(condition_name)
            else:
                self._console.log(f"{target.character._name} resisted the {condition_name} condition.")
        else:
            target.apply_condition(condition_name)

    def attack_saving_throw_damage(self, target):

        damage_type = self._damage[0]["damage_type"]["index"]
        damage_dice = self._damage[0]["damage_dice"]
        dc = self._dc["dc_value"]
        saving_throw_skill = self._dc["dc_type"]["index"]
        
        if dc:
            # Calculate saving throw roll
            saving_throw = Dice.roll_dice("1d20") + target.character.get_skill(saving_throw_skill) // 2
            self._console.log(f"Rolled a {saving_throw_skill} saving throw and got: {saving_throw}")
            
            # Apply damage based on success/failure of the saving throw
            if saving_throw < int(dc):
                # Failure: apply full damage
                self._apply_damage(target, damage_type, damage_dice)
            else:
                # Success: apply half damage
                if self._dc["success_type"] == "half":
                    self._apply_damage(target, damage_type, damage_dice, half_damage=True)
        else:
            # No saving throw needed, just apply full damage
            self._apply_damage(target, damage_type, damage_dice)

    def _apply_damage(self, target, damage_type, damage_dice, half_damage=False):
        # Roll damage dice and apply damage to the target
        damage = Dice.roll_dice(damage_dice)
        if half_damage:
            damage //= 2
        target.status_tracker.damage(damage, damage_type)

        # Log the damage dealt
        self._console.log(f"Dealt {damage} {damage_type} damage to {target.character._name}")


    def is_name_and_description_only(self):
        # Check if all other fields are None or empty
        return (
            self._name is not None and
            self._description is not None and
            not any([self._usage, self._bonus, self._dc, self._damage, self._options])
        )
    
    def get_condition(self):
        # Iterate over the conditions to check if any of them are mentioned in the description
        for condition in Ruleset.conditions.keys():
            if re.search(rf"\b{condition}\b", self._description, re.IGNORECASE):
                # Search for a DC value and the associated ability (e.g., "DC 10 Constitution saving throw")
                saving_throw_match = re.search(r"DC (\d+) (\w+)", self._description)
                
                if saving_throw_match:
                    # Extract the DC value and associated ability
                    dc_value = saving_throw_match.group(1)
                    saving_throw_skill = saving_throw_match.group(2).capitalize()  # Capitalize the ability name
                    return condition, dc_value, saving_throw_skill
                else:
                    # If no DC value found, just return the condition
                    return condition, None, None
        return None, None, None  # Return None if no condition is found

    def __repr__(self):
        return (
            f"Action(name={self._name!r}, description={self._description!r}, "
            f"usage={self._usage!r}, bonus={self._bonus!r}, "
            f"dc={self._dc!r}, damage={self._damage!r}, options={self._options!r})\n"
        )
    
    def __str__(self):
        return self._name