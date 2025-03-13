#!/usr/bin/env python
"""
Defines the Gorilla class for the Gorilla game,
attempting to mimic the original QBasic GORILLA.BAS shape and arms.
"""

import math
import pygame
from qbdraw import QBDraw

class Gorilla:
    # Arms state constants
    RIGHT_UP = 1
    LEFT_UP = 2
    ARMS_DOWN = 3

    def __init__(self, x: float, y: float, arms_state: int = ARMS_DOWN):
        """
        Initialize a Gorilla object with position, arms state, colors, and scale.
        
        :param x: The reference X coordinate of the Gorilla (screen coordinates)
        :param y: The reference Y coordinate of the Gorilla (screen coordinates)
        :param arms_state: Defines the gorilla's initial arms state (default: ARMS_DOWN)
        """
        self.x = x
        self.y = y
        self.arms_state = arms_state
        self.body_color = (139, 69, 19)  # Brownish color
        self.outline_color = (0, 0, 0)   # Black
        self.scale = 3.0  # Scaling factor

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the gorilla on the given Pygame surface using QBasic-like commands.
        
        :param surface: The Pygame surface to draw on
        """
        # Create QBDraw instance with the gorilla's position and scale
        drawer = QBDraw(surface, offset_x=self.x, offset_y=self.y, scale=self.scale)

        # Draw head (two filled rectangles)
        drawer.LINE(-4, 0, 3, 6, self.body_color, box=True, fill=True)
        drawer.LINE(-5, 2, 4, 4, self.body_color, box=True, fill=True)

        # Draw eyes/brow (horizontal line)
        drawer.LINE(-3, 2, 2, 2, self.outline_color)

        # Draw nose (four points)
        for i in [-2, -1, 1, 2]:
            drawer.PSET(i, 4, self.outline_color)

        # Draw neck (horizontal line)
        #print(f"drawer.LINE(-3, 7, 2, 7, self.body_color) scale={self.scale}")
        drawer.LINE(-3, 7, 2, 7, self.body_color)

        # Draw body (two filled rectangles)
        drawer.LINE(-8, 8, 7, 14, self.body_color, box=True, fill=True)
        drawer.LINE(-6, 15, 5, 20, self.body_color, box=True, fill=True)

        # Draw legs (series of arcs)
        for i in range(5):
            # Right leg arc
            drawer.CIRCLE(i, 25, 10, self.body_color, 3 * math.pi / 4, 9 * math.pi / 8)
            # Left leg arc
            drawer.CIRCLE(-6 + i, 25, 10, self.body_color, 15 * math.pi / 8, math.pi / 4)

        # Draw chest (two semi-circles)
        drawer.CIRCLE(-5, 10, 5, self.outline_color, 3 * math.pi / 2, 0)  # Left chest
        drawer.CIRCLE(5, 10, 5, self.outline_color, math.pi, 3 * math.pi / 2)  # Right chest

        # Draw arms (multiple arcs based on arms_state)
        for i in range(-5, 0):
            if self.arms_state == self.RIGHT_UP:
                # Left arm down
                drawer.CIRCLE(i, 14, 9, self.body_color, 3 * math.pi / 4, 5 * math.pi / 4)
                # Right arm up
                drawer.CIRCLE(5 + i, 4, 9, self.body_color, 7 * math.pi / 4, math.pi / 4)
            elif self.arms_state == self.LEFT_UP:
                # Left arm up
                drawer.CIRCLE(i, 4, 9, self.body_color, 3 * math.pi / 4, 5 * math.pi / 4)
                # Right arm down
                drawer.CIRCLE(5 + i, 14, 9, self.body_color, 7 * math.pi / 4, math.pi / 4)
            else:  # ARMS_DOWN
                # Both arms down
                drawer.CIRCLE(i, 14, 9, self.body_color, 3 * math.pi / 4, 5 * math.pi / 4)
                drawer.CIRCLE(5 + i, 14, 9, self.body_color, 7 * math.pi / 4, math.pi / 4)

    def set_arms_state(self, new_state: int) -> None:
        """
        Updates the arms state (1 = RIGHT_UP, 2 = LEFT_UP, 3 = ARMS_DOWN).
        
        :param new_state: The new arms state to set.
        """
        self.arms_state = new_state
