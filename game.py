import pygame
import button_actions as ba
from character_factory import CharacterFactory
from combatant import Combatant
from ui import UIManager
from button import Button
from ordered_group import OrderedDictGroup
from turn_manager import TurnManager
from random import choice

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((1500, 900))
        pygame.display.set_caption("DNDJRPGCEPS3000")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("./assets/PixelatedEleganceRegular.ttf", 20)
        self.running = True
        self.game_over = False

        self.background_image = pygame.image.load("./assets/bg.png")

        self.all_sprites = OrderedDictGroup()
        self.turn_manager = TurnManager()

        # UI
        self.ui = UIManager(self.screen, "Green")
        self.scroll_offset = 0
        self.ui_names = ["player1", "player2", "enemy1", "enemy2"]

        # Player
        pc_factory_ber = CharacterFactory(source_type="json", data="./data/berserker.json", x=150, y=200, console = self.ui.console, image_path="./assets/berserker.png")
        pc_factory_aco = CharacterFactory(source_type="json", data="./data/acolyte.json", x=150, y=400, console = self.ui.console, image_path="./assets/acolyte.png")
        player_ber = pc_factory_ber.get_character()
        player_aco = pc_factory_aco.get_character()
        self.ui.add_text("player1", str(player_ber), 10,650)
        self.ui.add_text("player2", str(player_aco), 10,30)
        self.all_sprites.add_with_key("Berserker",player_ber)
        self.all_sprites.add_with_key("Acolyte",player_aco)
        self.turn_manager.add_to_queue("Berserker")
        self.turn_manager.add_to_queue("Acolyte")

        # Enemies
        self.challenge_rating = 1
        self.player_names = ["Berserker", "Acolyte"]
        self.enemies: dict[str,Combatant] = {}
        self.target = ""
        self.add_enemy(1200, 200, self.challenge_rating)
        self.add_enemy(1200, 400, self.challenge_rating)
        self.ui.add_text("turn", str(self.turn_manager), 300,60)

        # Button
        button1 = Button(1300, 650, 150, 25, "Attack", self.font, "White", "Blue", False, action=lambda: ba.action_on_target(self.all_sprites[self.turn_manager.take_turn()],self.all_sprites[self.target]))
        button2 = Button(1300, 700, 150, 25, "Special", self.font, "White", "Blue", False, action=lambda: ba.special_on_target(self.all_sprites[self.turn_manager.take_turn()],self.all_sprites[self.target]))       
        self.ui.add_button("roll" ,button1)
        self.ui.add_button("heal" ,button2)
        

    def game_loop(self):
        while self.running:
            if self.game_over:
                self.show_game_over()
                break

            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(5)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Check if buttons were clicked
            self.ui.handle_event(event)
            if event.type == pygame.MOUSEWHEEL:
                self.scroll_offset -= event.y * 20  # Adjust scrolling speed
                self.scroll_offset = max(0, min(self.scroll_offset, 600))
            # Check if someone was selected
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_sprite_click(event)
                self.check_level_status()

        if not self.turn_manager.is_player_turn():
            self.cpu_turn()
            self.check_level_status()

    def handle_sprite_click(self, event):
        if self.ui.need_target():
            for sprite in self.all_sprites:
                self.target = sprite.handle_click(event.pos)
                if self.target:
                    self.ui.act_with_target()
                    self.target = ""

    def cpu_turn(self):
        
        for _ in range(len(self.enemies)):
            enemy_name = self.turn_manager.take_turn()
            cpu_target = choice(self.player_names)
            self.all_sprites[enemy_name].use_random_action(self.all_sprites[cpu_target])

    def update(self):
        self.check_combatant_status()
        self.all_sprites.update()
        self.ui.update_text("player1", str(self.all_sprites.get("Berserker")))
        self.ui.update_text("player2", str(self.all_sprites.get("Acolyte")))
        self.ui.update_text("turn", str(self.turn_manager))
        for i, key in enumerate(self.enemies):
            self.ui.update_text(f"enemy{i+1}", str(self.enemies[key]))
        self.textbox_surface = self.ui.update_console()
        self.check_level_status()

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.all_sprites.draw(self.screen)
        self.ui.draw()
        pygame.draw.rect(self.screen, "Black", pygame.Rect(10,10, 900, 150), 0)
        self.screen.blit(self.textbox_surface, (10, 10), (0, self.scroll_offset, 900, 150))
        pygame.draw.rect(self.screen, "White", pygame.Rect(10,10, 900, 150), 2)  # Outline the text box
        pygame.display.flip()

    def add_enemy(self, x, y, challenge_rating):
        while True:
            npc_factory = CharacterFactory(source_type="api", data=challenge_rating, x=x, y=y, console=self.ui.console)
            npc = npc_factory.get_character()
            npc_name = npc.character._name
            print(npc_name)
            if npc_name not in self.all_sprites.keys():    
                break  

        self.all_sprites.add_with_key(npc.character._name, npc)
        self.turn_manager.add_to_queue(npc.character._name)
        self.enemies[npc.character._name] = npc
        self.ui.add_text(f"enemy{self.enemies.__len__()}", str(self.enemies[npc.character._name]),10, 30)

    def remove_combatant(self,combat_name, ui_name):
        self.all_sprites.__delitem__(combat_name)
        self.turn_manager.remove_from_queue(combat_name)
        self.ui.update_text(ui_name, "")
        if combat_name in self.player_names:
            self.player_names.remove(combat_name)
        if combat_name in self.enemies:
            self.enemies.pop(combat_name)
        if combat_name in self.ui_names:
            self.ui_names.remove(ui_name)

    def check_combatant_status(self):
        # Create a list of current items to avoid modifying the dictionary while iterating
        combatants = list(zip(self.ui_names, self.all_sprites.values()))
        for name, sprite in combatants:
            if sprite.status_tracker.is_dead():
                self.remove_combatant(sprite.character._name , name)

    def check_level_status(self):
        if len(self.player_names) == 0:
            self.game_over = True
        if len(self.enemies) == 0:
            self.set_up_level()

    def set_up_level(self):
        self.challenge_rating += 1
        self.add_enemy(1200, 200, self.challenge_rating)
        self.add_enemy(1200, 400, self.challenge_rating)

    def show_game_over(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill("Black")
            game_over_text = self.font.render(f"Game Over. Score: {self.challenge_rating * 100}", True, "White")
            self.screen.blit(game_over_text, (500, 450))
            pygame.display.flip()

