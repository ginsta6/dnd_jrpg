import requests
from random import randint


class Monster():
    def __init__(self):
        data = self.pull_monster_data(21)
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
        self._abilities = data["special_abilities"]
        self._actions = data["actions"]
        self._legen_actions = data["legendary_actions"]

    def pull_monster_data(self, ch):
        dnd_url = "https://www.dnd5eapi.co/api/monsters"
        headers = {"Accept": "application/json"}

        challenge_rating = f"?challenge_rating={ch}"
        response = requests.get(url=dnd_url + challenge_rating, headers=headers).json()
        monster_dict = response["results"]
        monster_nr = randint(0, response["count"] - 1)
        monster_index ="/" + monster_dict[monster_nr]["index"]
        return requests.get(url=dnd_url + monster_index, headers=headers).json()
    
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
    
    def __str__(self):
        return f"{self._name} - {self._type} - HP: {self._hp} - AC: {self._ac}"
