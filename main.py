from character import Character
import pygame

def main():
    print("Welcome to the Dungeos And Dragons Japaneese Role Playing Game Combat Encounter Player System 3000\nor DNDJRPGCEPS3000, for short\n")
    pygame.init()

    monster = Character.create_monster(2)

    player = Character.create_player("./data/berserker.json")

    game(player, monster)

def game(player, monster):
    # Set up display
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("DNDJRPGCEPS3000")

    # Define color
    white = (255, 255, 255)
    black = (0, 0, 0)

    font = pygame.font.SysFont("Arial", 12)

    text_p = font.render(str(player), True, white)
    text_m = font.render(str(monster), True, white)

    # Game loop
    running = True
    spacebar_pressed = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not spacebar_pressed:
                    # Trigger the action when spacebar is pressed
                    player.actions[0].use_action(monster)
                    text_m = font.render(str(monster), True, white)
                    spacebar_pressed = True  # Set the flag to prevent multiple presses

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    # Reset the flag when the spacebar is released
                    spacebar_pressed = False

        # Draw a red rectangle
        screen.fill(black)

        screen.blit(text_p, (50,100))
        screen.blit(text_m, (50,80))
        

        # Update display
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()