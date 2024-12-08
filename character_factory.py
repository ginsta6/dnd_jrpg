import json
import requests
from character import Character
from status_tracker import StatusTracker
from combatant import Combatant
from random import randint

class CharacterFactory():
    def __init__(self, source_type, data, x, y):
        self.character = None
        self.status_tracker = None
        self.combatant = None

        if source_type == "json":
            self.create_from_json(data, x, y)
        elif source_type == "api":
            self.create_from_api(data, x, y)

    def create_from_json(self, file_name, x, y):
        with open(file_name, "r") as file:
            character_data = json.load(file)

        self.create_character(character_data, x, y)

    def create_from_api(self, ch_rating, x, y):
        dnd_url = "https://www.dnd5eapi.co/api/monsters"
        headers = {"Accept": "application/json"}

        challenge_rating = f"?challenge_rating={ch_rating}"
        response = requests.get(url=dnd_url + challenge_rating, headers=headers).json()
        monster_dict = response["results"]
        monster_nr = randint(0, response["count"] - 1)
        monster_index ="/" + monster_dict[monster_nr]["index"]

        character_data = requests.get(url=dnd_url + monster_index, headers=headers).json()

        self.create_character(character_data, x ,y)


    def create_character(self, character_data, x, y):
        self.character = Character(character_data)
        self.status_tracker = StatusTracker(self.character)
        self.combatant = Combatant(x,y,self.character,self.status_tracker)
        
    def get_character(self) -> Combatant:
        return self.combatant