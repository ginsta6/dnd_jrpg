import pygame
import button_actions as ba
from character_factory import CharacterFactory
from combatant import Combatant
from ui import UIManager
from button import Button

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 500))
        pygame.display.set_caption("DNDJRPGCEPS3000")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("./assets/PixelatedEleganceRegular.ttf", 20)
        self.running = True

        self.all_sprites = pygame.sprite.Group()

        # Player
        self.pc_factory = CharacterFactory(source_type="json", data="./data/berserker.json", x=200, y=200)
        self.player = self.pc_factory.get_character()
        self.all_sprites.add(self.player)

        # UI
        self.ui = UIManager(self.screen, self.font, "Green")
        self.ui.add_text("player", str(self.player), 10,10)

        # Enemies
        self.enemies: dict[str,Combatant] = {}
        self.target = ""
        self.add_enemy(200, 300)
        self.add_enemy(300, 300)

        # Button
        button1 = Button(100, 100, 200, 50, "Roll to hit", self.font, "White", "Blue", False, action=lambda: ba.action_on_target(self.player,self.enemies[self.target]))
        button2 = Button(400, 100, 200, 50, "Potion", self.font, "White", "Blue", True, action=lambda: ba.heal_target(self.player))        
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

            # Check if someone was selected
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.ui.button_elements["roll"].clicked:
                    for sprite in self.all_sprites:
                        self.target = sprite.handle_click(event.pos)
                        if self.target:
                            self.ui.button_elements["roll"].action()
                            self.ui.button_elements["roll"].clicked = False
                            self.target = ""


    def update(self):
        self.all_sprites.update()
        self.ui.update_text("player", str(self.player))
        for i, key in enumerate(self.enemies):
            self.ui.update_text(f"enemy{i+1}", str(self.enemies[key]))

    def draw(self):
        self.screen.fill("Black")
        self.all_sprites.draw(self.screen)
        self.ui.draw()
        pygame.display.flip()

    def add_enemy(self, x, y):
        npc_factory = CharacterFactory(source_type="api", data="2", x=x, y=y)
        npc = npc_factory.get_character()

        self.all_sprites.add(npc)
        self.enemies[npc.character._name] = npc
        self.ui.add_text(f"enemy{self.enemies.__len__()}", str(self.enemies[npc.character._name]),10, 30)