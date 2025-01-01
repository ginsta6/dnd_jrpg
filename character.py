import requests
import json
from random import randint
from action import Action


class Character():
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
        with open(filename, "r") as file:
            data = json.load(file)
        return cls(data)

    @classmethod
    def create_monster(cls, challenge_rating: int):
        data = cls.pull_monster_data(challenge_rating)
        return cls(data)

    @classmethod
    def pull_monster_data(cls, ch):
        dnd_url = "https://www.dnd5eapi.co/api/monsters"
        headers = {"Accept": "application/json"}

        challenge_rating = f"?challenge_rating={ch}"
        response = requests.get(url=dnd_url + challenge_rating, headers=headers).json()
        monster_dict = response["results"]
        monster_nr = randint(0, response["count"] - 1)
        monster_index ="/" + monster_dict[monster_nr]["index"]

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
            prof_list.append({"name": prof["proficiency"]["name"], "value": prof["value"]})
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
        if my_attributes["can_take_actions"] == False:
            self._console.log(f"{self._name} can't do that right now")
            return
        action_string = f"{self._name} is using {self.actions[action_id]} againgst {target.character._name}"
        self._console.log(action_string)
        if my_attributes["attack_advantage"] == my_attributes["attack_disadvantage"]: #both cancel out or none
            self.actions[action_id].use_action(target, 0)
        elif my_attributes["attack_advantage"]:
            self.actions[action_id].use_action(target, 1)
            # adv
        elif my_attributes["attack_disadvantage"]:
            self.actions[action_id].use_action(target, -1)
            # dis

    def check_action(self, action_id):
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
        return (f"Name: {self._name}\n"
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
                    f"Legendary Actions: {self._legen_actions if self._legen_actions else 'None'}")
    
