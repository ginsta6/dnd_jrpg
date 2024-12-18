import pygame
import button_actions as ba
from character_factory import CharacterFactory
from combatant import Combatant
from ui import UIManager
from button import Button
from ordered_group import OrderedDictGroup
from random import choice

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((1500, 900))
        pygame.display.set_caption("DNDJRPGCEPS3000")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("./assets/PixelatedEleganceRegular.ttf", 20)
        self.running = True

        self.all_sprites = OrderedDictGroup()

        # Player
        pc_factory_ber = CharacterFactory(source_type="json", data="./data/berserker.json", x=150, y=200, image_path="./assets/berserker.png")
        pc_factory_aco = CharacterFactory(source_type="json", data="./data/acolyte.json", x=150, y=400, image_path="./assets/acolyte.png")
        player_ber = pc_factory_ber.get_character()
        player_aco = pc_factory_aco.get_character()
        self.all_sprites.add_with_key("Berserker",player_ber)
        self.all_sprites.add_with_key("Acolyte",player_aco)
        self.player_turn = True

        # UI
        self.ui = UIManager(self.screen, "Green")
        self.ui.add_text("player1", str(player_ber), 10,650)
        self.ui.add_text("player2", str(player_aco), 10,30)
        self.scroll_offset = 0

        # Enemies
        self.enemies: dict[str,Combatant] = {}
        self.target = ""
        self.add_enemy(1200, 200)
        self.add_enemy(1200, 400)

        # Button
        button1 = Button(800, 650, 150, 25, "Attack", self.font, "White", "Blue", False, action=lambda: ba.action_on_target(self.all_sprites[self.all_sprites["Berserker"].character._name],self.all_sprites[self.target]))
        button2 = Button(800, 700, 150, 25, "Potion", self.font, "White", "Blue", False, action=lambda: ba.heal_target(self.all_sprites[self.target]))        
        self.ui.add_button("roll" ,button1)
        self.ui.add_button("heal" ,button2)
        

    def game_loop(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

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

        if not self.player_turn:
            self.cpu_turn()

    def handle_sprite_click(self, event):
        if self.ui.need_target():
            for sprite in self.all_sprites:
                self.target = sprite.handle_click(event.pos)
                if self.target:
                    self.ui.act_with_target()
                    self.target = ""
                    self.player_turn = False

    def cpu_turn(self):
        names = ["Berserker", "Acolyte"]
        for enemy in self.enemies.values():
            cpu_target = choice(names)
            self.ui.add_to_console(enemy.use_random_action(self.all_sprites[cpu_target]) + f"against {cpu_target}")
        self.player_turn = True

    def update(self):
        self.all_sprites.update()
        self.ui.update_text("player1", str(self.all_sprites["Berserker"]))
        self.ui.update_text("player2", str(self.all_sprites["Acolyte"]))
        for i, key in enumerate(self.enemies):
            self.ui.update_text(f"enemy{i+1}", str(self.enemies[key]))
        self.textbox_surface = self.ui.update_console()

    def draw(self):
        self.screen.fill("Black")
        self.all_sprites.draw(self.screen)
        self.ui.draw()
        self.screen.blit(self.textbox_surface, (10, 10), (0, self.scroll_offset, 900, 150))
        pygame.draw.rect(self.screen, "White", pygame.Rect(10,10, 900, 150), 2)  # Outline the text box
        pygame.display.flip()

    def add_enemy(self, x, y):
        npc_factory = CharacterFactory(source_type="api", data="2", x=x, y=y, image_path="./assets/aberration.png")
        npc = npc_factory.get_character()

        self.all_sprites.add_with_key(npc.character._name, npc)
        self.enemies[npc.character._name] = npc
        self.ui.add_text(f"enemy{self.enemies.__len__()}", str(self.enemies[npc.character._name]),10, 30)