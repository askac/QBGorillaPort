#!/usr/bin/env python
"""
Test script for Banana class, including physics and EGA/CGA sprite rendering.
"""

import pygame
import random
from banana import Banana
from graphics import Graphics
from physics import plot_shot

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 9.8
WIND = 0.0  # No wind for now

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Banana Test")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    # Initialize Graphics (handles banana rendering)
    graphics = Graphics(screen)

    # Test CGA / EGA mode
    use_ega = True  # Set to False if you want CGA mode

    # Banana storage
    bananas = []

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Generate a random banana with random angle/speed
                    angle_deg = random.randint(30, 70)
                    velocity = random.uniform(150.0, 300.0)

                    # Create a banana at bottom-left
                    banana = Banana(
                        x=50,
                        y=SCREEN_HEIGHT - 50,
                        angle_deg=angle_deg,
                        velocity=velocity,
                        gravity=GRAVITY,
                        wind=WIND
                    )
                    bananas.append(banana)

        # Update bananas
        for b in bananas:
            b.update(dt, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Remove bananas that are no longer flying
        bananas = [b for b in bananas if b.alive]

        # Render everything
        screen.fill((135, 206, 235))  # Sky blue

        # Draw all bananas
        for b in bananas:
            if use_ega:
                b.draw(screen, graphics, "banana_right")  # EGA banana
            else:
                b.draw(screen, graphics, b.rotation_step % 4)  # CGA rotation

        # Debug info
        debug_text = f"Bananas: {len(bananas)} | Mode: {'EGA' if use_ega else 'CGA'}"
        text_surf = font.render(debug_text, True, (255, 255, 255))
        screen.blit(text_surf, (10, 10))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

