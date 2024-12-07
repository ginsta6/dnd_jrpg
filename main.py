import pygame
from sys import exit
from game import Game

def main():
    print("Welcome to the Dungeos And Dragons Japaneese Role Playing Game Combat Encounter Player System 3000\nor DNDJRPGCEPS3000, for short\n")
    
    pygame.init()
    mygame = Game()
    mygame.game_loop()
    pygame.quit()
    exit()

if __name__ == "__main__":
    main()