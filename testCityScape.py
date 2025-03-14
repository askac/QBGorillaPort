#!/usr/bin/env python3
import pygame
from cityscape import CityScape

def main():
    pygame.init()
    screen_width, screen_height = 640, 480
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("CityScape Test - With Windows")
    clock = pygame.time.Clock()

    # Generate a cityscape with windows
    city = CityScape(screen_width, screen_height, num_buildings=10)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Press 'R' to regenerate cityscape
                    city.generate_buildings()

        # Clear screen
        screen.fill((135, 206, 235))  # Sky blue

        # Draw cityscape
        city.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
