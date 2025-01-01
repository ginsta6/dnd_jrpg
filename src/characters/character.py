import requests
import json
from random import randint
from characters.action import Action


class Character:
    def __init__(self, data: dict, console):
        self._name = data["name"]
        self._type = data["type"]
        self._hp = data["hit_points"]
        self._ac = data["armor_class"][0]["value"]
        self._str = data["strength"]
        self._dex = data["dexterity"]
        self._con = data["constitution"]
        self._int = data["intelligence"]
        self._wis = data["wisdom"]
        self._cha = data["charisma"]
        self.proficiencies = data["proficiencies"]
        self._prof_bonus = data["proficiency_bonus"]
        self._damage_resistances = data["damage_resistances"]
        self._damage_immunities = data["damage_immunities"]
        self.condition_immunities = data["condition_immunities"]
        self.contitions = []
        self._abilities = data["special_abilities"]
        self.actions = (data["actions"] + data["special_abilities"], console)
        self.legen_actions = (data["legendary_actions"], console)

        self._console = console

    @classmethod
    def create_player(cls, filename: str):
        """Create a player character from a JSON file."""
        with open(filename, "r") as file:
            data = json.load(file)
        return cls(data)

    @classmethod
    def create_monster(cls, challenge_rating: int):
        """Create a monster character from the D&D 5e API."""
        data = cls.pull_monster_data(challenge_rating)
        return cls(data)

    @classmethod
    def pull_monster_data(cls, ch):
        """Pull monster data from the D&D 5e API."""
        dnd_url = "https://www.dnd5eapi.co/api/monsters"
        headers = {"Accept": "application/json"}

        challenge_rating = f"?challenge_rating={ch}"
        response = requests.get(url=dnd_url + challenge_rating, headers=headers).json()
        monster_dict = response["results"]
        monster_nr = randint(0, response["count"] - 1)
        monster_index = "/" + monster_dict[monster_nr]["index"]

        return requests.get(url=dnd_url + monster_index, headers=headers).json()

    @property
    def actions(self):
        return self._actions

    @actions.setter
    def actions(self, value):
        data, console = value
        self._actions = []
        for entry in data:
            self._actions.append(Action(entry, console))
        self.add_multiattack()

    def add_multiattack(self):
        """Add individual attacks to the Multiattack action options."""
        for action in self._actions:
            if action._name == "Multiattack":
                # Process the Multiattack and add the individual attacks to options
                for (
                    multiattack_action
                ) in action._actions:  # Look at each sub-action in Multiattack
                    action_name = multiattack_action["action_name"]
                    action_count = int(multiattack_action["count"])
                    for _ in range(action_count):
                        matched_attacks = [
                            attack
                            for attack in self._actions
                            if attack._name == action_name
                        ]
                        action._options.extend(matched_attacks)

    @property
    def legen_actions(self):
        return self._legen_actions

    @legen_actions.setter
    def legen_actions(self, value):
        data, console = value
        self._legen_actions = []
        for entry in data:
            self.legen_actions.append(Action(entry, console))

    @property
    def proficiencies(self):
        return self._proficiencies

    @proficiencies.setter
    def proficiencies(self, data):
        prof_list = []
        for prof in data:
            prof_list.append(
                {"name": prof["proficiency"]["name"], "value": prof["value"]}
            )
        self._proficiencies = prof_list

    @property
    def condition_immunities(self):
        return self._condition_immunities

    @condition_immunities.setter
    def condition_immunities(self, data):
        cond_list = []
        for cond in data:
            cond_list.append(cond["name"])
        self._condition_immunities = cond_list

    @property
    def ac(self):
        return self._ac

    @property
    def hp(self):
        return self._hp

    def use_action(self, action_id, target, my_attributes):
        """Use the specified action"""
        if not my_attributes.get("can_take_actions", True):
            self._console.log(f"{self._name} can't do that right now")
            return

        action_name = self.actions[action_id]
        target_name = target.character._name
        self._console.log(f"{self._name} is using {action_name} against {target_name}")

        target_attributes = target.status_tracker.attributes

        # Determine advantage or disadvantage
        advantage = my_attributes.get(
            "attack_advantage", False
        ) or target_attributes.get("attackers_have_advantage", False)
        disadvantage = my_attributes.get(
            "attack_disadvantage", False
        ) or target_attributes.get("attackers_have_disadvantage", False)

        # Calculate final advantage state
        if advantage and disadvantage:
            advantage_state = 0  # Both cancel out
        elif advantage:
            advantage_state = 1  # Advantage
        elif disadvantage:
            advantage_state = -1  # Disadvantage
        else:
            advantage_state = 0  # Neutral

        # Use the action with the calculated advantage state
        self.actions[action_id].use_action(target, advantage_state)

    def check_action(self, action_id):
        """Check if the action is a name and description only action."""
        return self.actions[action_id].is_name_and_description_only()

    def get_skill(self, skill_name: str):
        """Returns the ability score corresponding to a skill or saving throw."""
        skill_name = skill_name.lower()

        skill_map = {
            "strength": self._str,
            "str": self._str,  # shorthand for strength
            "dexterity": self._dex,
            "dex": self._dex,  # shorthand for dexterity
            "constitution": self._con,
            "con": self._con,  # shorthand for constitution
            "intelligence": self._int,
            "int": self._int,  # shorthand for intelligence
            "wisdom": self._wis,
            "wis": self._wis,  # shorthand for wisdom
            "charisma": self._cha,
            "cha": self._cha,  # shorthand for charisma
        }

        # Check if the skill is part of the stat abilities
        if skill_name in skill_map:
            return skill_map[skill_name]

    def __repr__(self):
        return (
            f"Name: {self._name}\n"
            f"Type: {self._type}\n"
            f"HP: {self._hp}\n"
            f"AC: {self._ac}\n"
            f"Strength: {self._str}\n"
            f"Constitution: {self._con}\n"
            f"Intelligence: {self._int}\n"
            f"Wisdom: {self._wis}\n"
            f"Charisma: {self._cha}\n"
            f"Proficiencies: {self.proficiencies if self.proficiencies else 'None'}\n"
            f"Proficiency Bonus: {self._prof_bonus}\n"
            f"Damage Resistances: {self._damage_resistances if self._damage_resistances else 'None'}\n"
            f"Damage Immunities: {self._damage_immunities if self._damage_immunities else 'None'}\n"
            f"Condition Immunities: {self.condition_immunities if self.condition_immunities else 'None'}\n"
            f"Abilities: {self._abilities if self._abilities else 'None'}\n"
            f"Actions: {self._actions if self._actions else 'None'}\n"
            f"Legendary Actions: {self._legen_actions if self._legen_actions else 'None'}"
        )
