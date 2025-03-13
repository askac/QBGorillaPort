#!/usr/bin/env python3
import pygame
from gorilla import Gorilla

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    # Create a gorilla at position (100, 200) with arms down
    gorilla = Gorilla(100, 200, Gorilla.ARMS_DOWN)
    gorilla2 = Gorilla(200, 200, Gorilla.ARMS_DOWN)
    gorilla3 = Gorilla(350, 200, Gorilla.ARMS_DOWN)
    gorilla.scale = 1.0
    gorilla2.scale = 3.0
    gorilla3.scale = 6.0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    gorilla.set_arms_state(Gorilla.RIGHT_UP)
                    gorilla2.set_arms_state(Gorilla.RIGHT_UP)
                    gorilla3.set_arms_state(Gorilla.RIGHT_UP)
                elif event.key == pygame.K_2:
                    gorilla.set_arms_state(Gorilla.LEFT_UP)
                    gorilla2.set_arms_state(Gorilla.LEFT_UP)
                    gorilla3.set_arms_state(Gorilla.LEFT_UP)

                elif event.key == pygame.K_3:
                    gorilla.set_arms_state(Gorilla.ARMS_DOWN)
                    gorilla2.set_arms_state(Gorilla.ARMS_DOWN)
                    gorilla3.set_arms_state(Gorilla.ARMS_DOWN)

        # Clear screen
        screen.fill((135, 206, 235))  # sky-like background
        
        # Draw the gorilla
        gorilla.draw(screen)
        gorilla2.draw(screen)
        gorilla3.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
