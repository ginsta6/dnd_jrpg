import pygame
from character import Character
from player import Player
from ui import UIManager
from button import Button

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 500))
        pygame.display.set_caption("DNDJRPGCEPS3000")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        self.running = True

        self.all_sprites = pygame.sprite.Group()

        # Player
        self.player = Player(375, 275)
        self.all_sprites.add(self.player)

        # UI
        self.ui = UIManager(self.screen, self.font, "Blue")
        self.ui.add_text("player", str(self.player.character), 10,10)

        # Enemies
        self.enemies = []
        self.add_enemy()

        # Button
        self.button = Button(100, 100, 200, 50, "Roll to hit", self.font, "White", "Blue", action=lambda: self.button_click())
        

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
            self.button.handle_event(event)


    def update(self):
        self.all_sprites.update()
        self.ui.update_text("enemy1", str(self.enemies[0]))

    def draw(self):
        self.screen.fill("Black")
        self.all_sprites.draw(self.screen)
        self.ui.draw()
        self.button.draw(self.screen)
        pygame.display.flip()

    def add_enemy(self):
        self.enemies.append(Character.create_monster(2))
        self.ui.add_text("enemy1", str(self.enemies[0]),10, 30)

    def button_click(self):
        self.player.character.actions[0].use_action(self.enemies[0])