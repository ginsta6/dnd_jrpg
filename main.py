import pygame
from sys import exit
from game import Game

def main():
    print("Welcome to the Dungeos And Dragons Japaneese Role Playing Game Combat Encounter Player System \nor DNDJRPGCEPS, for short\n")
    
    pygame.init()
    mygame = Game()
    mygame.game_loop()
    pygame.quit()
    exit()

if __name__ == "__main__":
    main()