import pygame
from character import Character

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50,50))
        self.image.fill("Blue")
        self.rect = self.image.get_rect(topleft=(x,y))
        self.character = Character.create_player("./data/berserker.json")


    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

    def update(self):
        self.handle_input()