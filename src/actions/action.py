from src.utils.dice import Dice
from src.utils.console import Console
from src.utils.rules import Ruleset
from random import choice
import re


class Action:
    def __init__(self, data: dict, console: Console):
        self._console = console
        self._name = data.get("name")
        self._description = data.get("desc")
        self._usage = data.get("usage")
        self._bonus = data.get("attack_bonus")
        self._dc = data.get("dc")  
        self._damage = data.get("damage")
        self._options = self._set_options(data.get("options"), console)
        self._actions = data.get("actions")

    def use_action(self, target, advantage: int):
        """
        Executes the action. Depending on the type of action, different logic is applied.

        Args:
            target: The target of the action. Combatant object.
            advantage: Modifier for advantage/disadvantage during the action.
        """
        if self._name == "Multiattack":
            # Multiattack algorithm
            self._multiattack(target, advantage)

        elif self._options:
            # Choose a random option and use it as the action
            random_option = choice(self._options)
            self._console.log(f"{self._name} chose {random_option._name}")
            random_option.use_action(target, advantage)

        elif self._dc:
            # Special use algorithm (saving throw for target)
            self._special_attack(target)

        elif self._damage:
            # Regular attack algorithm
            damage_type = self._damage[0]["damage_type"]["index"]
            if damage_type == "healing":
                self._healing_attack(target)
            else:
                self._regular_attack(target, advantage)

        else:
            self._console.log(f"Action {self._name} has no executable logic.")

    def _multiattack(self, target, advantage: int):
        """For each attack in the multiattack, roll to hit and apply damage"""
        for attack in self._options:
            attack.use_action(target, advantage)

    def _healing_attack(self, target):
        """Heal the target for the specified amount of HP"""
        # Roll the healing dice and apply the healing to the target
        healing = Dice.roll_dice(self._damage[0]["damage_dice"])
        target.status_tracker.heal(healing)

        # Log the healing done
        self._console.log(f"Healed {target.character._name} for {healing} HP.")

    def _special_attack(self, target):
        """Special attack that requires a saving throw from the target"""
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
        """Roll to hit and apply damage to the target"""
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
        """Apply a condition to the target if they fail a saving throw"""
        condition_name, dc, saving_throw_skill = condition
        if dc:
            saving_throw = (
                Dice.roll_dice("1d20")
                + target.character.get_skill(saving_throw_skill) // 2
            )
            self._console.log(
                f"Rolled a {saving_throw_skill} saving throw and got: {saving_throw}"
            )
            if saving_throw < int(dc):
                target.apply_condition(condition_name)
            else:
                self._console.log(
                    f"{target.character._name} resisted the {condition_name} condition."
                )
        else:
            target.apply_condition(condition_name)

    def attack_saving_throw_damage(self, target):
        """Apply damage to the target based on a saving throw"""
        damage_type = self._damage[0]["damage_type"]["index"]
        damage_dice = self._damage[0]["damage_dice"]
        dc = self._dc["dc_value"]
        saving_throw_skill = self._dc["dc_type"]["index"]

        if dc:
            # Calculate saving throw roll
            saving_throw = (
                Dice.roll_dice("1d20")
                + target.character.get_skill(saving_throw_skill) // 2
            )
            self._console.log(
                f"Rolled a {saving_throw_skill} saving throw and got: {saving_throw}"
            )

            # Apply damage based on success/failure of the saving throw
            if saving_throw < int(dc):
                # Failure: apply full damage
                self._apply_damage(target, damage_type, damage_dice)
            else:
                # Success: apply half damage
                if self._dc["success_type"] == "half":
                    self._apply_damage(
                        target, damage_type, damage_dice, half_damage=True
                    )
        else:
            # No saving throw needed, just apply full damage
            self._apply_damage(target, damage_type, damage_dice)

    def _apply_damage(self, target, damage_type, damage_dice, half_damage=False):
        """Apply damage to the target based on the damage dice and type"""
        # Roll damage dice and apply damage to the target
        damage = Dice.roll_dice(damage_dice)
        if half_damage:
            damage //= 2
        target.status_tracker.damage(damage, damage_type)

        # Log the damage dealt
        self._console.log(
            f"Dealt {damage} {damage_type} damage to {target.character._name}"
        )

    def is_name_and_description_only(self):
        """Check if the action is only a name and description"""
        # Check if all other fields are None or empty
        return (
            self._name is not None
            and self._description is not None
            and not any(
                [self._usage, self._bonus, self._dc, self._damage, self._options]
            )
        )

    def get_condition(self):
        """Check if the description contains a condition and return it"""
        if self._description is None:
            return None, None, None

        # Iterate over the conditions to check if any of them are mentioned in the description
        for condition in Ruleset.conditions.keys():
            if re.search(rf"\b{condition}\b", self._description, re.IGNORECASE):
                # Search for a DC value and the associated ability (e.g., "DC 10 Constitution saving throw")
                saving_throw_match = re.search(r"DC (\d+) (\w+)", self._description)

                if saving_throw_match:
                    # Extract the DC value and associated ability
                    dc_value = saving_throw_match.group(1)
                    saving_throw_skill = saving_throw_match.group(
                        2
                    ).capitalize()  # Capitalize the ability name
                    return condition, dc_value, saving_throw_skill
                else:
                    # If no DC value found, just return the condition
                    return condition, None, None
        return None, None, None  # Return None if no condition is found

    def _set_options(self, options_data, console):
        """Setter method for _options. Converts the raw 'options' data into a list of Action objects."""
        if not options_data:
            return []

        options = []
        for option in options_data["from"]["options"]:
            if isinstance(
                option, dict
            ):  # Check if the option is structured as an Action-like dictionary
                options.append(Action(option, console))
            else:
                self._console.log(f"Invalid option format: {option}")

        return options

    def __repr__(self):
        return (
            f"Action(name={self._name!r}, description={self._description!r}, "
            f"usage={self._usage!r}, bonus={self._bonus!r}, "
            f"dc={self._dc!r}, damage={self._damage!r}, options={self._options!r})"
            f"actions={self._actions}\n"
        )

    def __str__(self):
        return self._name
