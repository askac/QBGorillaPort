#!/usr/bin/env python3
import pygame
from gorilla_old import Gorilla

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    # Create a gorilla at position (100, 200) with arms down
    gorilla = Gorilla(100, 200, Gorilla.ARMS_DOWN)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    gorilla.set_arms_state(Gorilla.RIGHT_UP)
                elif event.key == pygame.K_2:
                    gorilla.set_arms_state(Gorilla.LEFT_UP)
                elif event.key == pygame.K_3:
                    gorilla.set_arms_state(Gorilla.ARMS_DOWN)

        # Clear screen
        screen.fill((135, 206, 235))  # sky-like background
        
        # Draw the gorilla
        gorilla.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
