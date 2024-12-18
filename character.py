import requests
import json
from random import randint
from action import Action


class Character():
    def __init__(self, data: dict):
        self._name = data["name"]
        self._type = data["type"]
        self._hp = data["hit_points"]
        self._ac = data["armor_class"][0]["value"]
        self._str = data["strength"]
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
        self.actions = data["actions"]
        self.legen_actions = data["legendary_actions"]

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
    def actions(self, data):
        self._actions = []
        for entry in data:
            self._actions.append(Action(entry))
    
    @property
    def legen_actions(self):
        return self._legen_actions
    
    @legen_actions.setter
    def legen_actions(self, data):
        self._legen_actions = []
        for entry in data:
            self.legen_actions.append(Action(entry))

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
        if my_attributes["attack_advantage"] == my_attributes["attack_disadvantage"]: #both cancel out or none
            self.actions[action_id].use_action(target, 0)
        elif my_attributes["attack_advantage"]:
            self.actions[action_id].use_action(target, 1)
            # adv
        elif my_attributes["attack_disadvantage"]:
            self.actions[action_id].use_action(target, -1)
            # dis
        return f"{self._name} is using {self.actions[action_id]}"
            

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
    
