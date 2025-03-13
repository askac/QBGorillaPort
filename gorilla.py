#!/usr/bin/env python
"""
Defines the Gorilla class for the Gorilla game,
attempting to mimic the original QBasic GORILLA.BAS shape and arms.
"""

import math
import pygame

class Gorilla:
    """
    Represents a Gorilla character with position, arms state,
    and a draw method that approximates the original GORILLA.bas visuals.
    """

    # Arms state constants (matching original GORILLA.bas logic)
    RIGHT_UP = 1   # Right arm up
    LEFT_UP = 2    # Left arm up
    ARMS_DOWN = 3  # Both arms down

    def __init__(self, x: float, y: float, arms_state: int = ARMS_DOWN):
        """
        :param x: The reference X coordinate of the Gorilla.
        :param y: The reference Y coordinate of the Gorilla.
        :param arms_state: Defines the gorilla's initial arms state.
        """
        self.x = x
        self.y = y
        self.arms_state = arms_state
        
        # Colors for the gorilla and outlines
        self.body_color = (139, 69, 19)   # Brownish color similar to "OBJECTCOLOR"
        self.outline_color = (0, 0, 0)    # Black
        self.scale = 3.0  # Scaling factor to enlarge/diminish the gorilla's size

    def _scl(self, n: float) -> int:
        """Helper method to mimic QBasic's Scl function for scaling coordinates."""
        return int(n * self.scale)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the gorilla on the given Pygame surface.
        :param surface: The Pygame surface to draw on.
        """
        # Adjust coordinates for Pygame (Y-axis is inverted)
        # In QBasic, Y increases downward; in Pygame, Y increases upward
        # We'll use the reference point (self.x, self.y) as the base of the gorilla

        # Draw head
        # First rectangle: from (x - Scl(4), y) to (x + Scl(2.9), y + Scl(6))
        # In Pygame: from (x - Scl(4), y - Scl(6)) with width Scl(4) + Scl(2.9), height Scl(6)
        head_width1 = self._scl(4) + self._scl(2.9)  # Approximately Scl(6.9)
        pygame.draw.rect(surface, self.body_color, 
                      (self.x - self._scl(4), self.y - self._scl(6), 
                       head_width1, self._scl(6)))

        # Second rectangle: from (x - Scl(5), y + Scl(2)) to (x + Scl(4), y + Scl(4))
        # In Pygame: from (x - Scl(5), y - Scl(4)) with width Scl(5) + Scl(4), height Scl(2)
        head_width2 = self._scl(5) + self._scl(4)  # Scl(9)
        pygame.draw.rect(surface, self.body_color, 
                       (self.x - self._scl(5), self.y - self._scl(4), 
                       head_width2, self._scl(2)))

        # Draw eyes/brow
        pygame.draw.line(surface, self.outline_color, 
                     (self.x - self._scl(3), self.y - self._scl(4)),  # Adjusted to align with head
                     (self.x + self._scl(2), self.y - self._scl(4)), 1)

        # Draw nose
        pygame.draw.circle(surface, self.outline_color, 
                       (int(self.x - self._scl(2)), int(self.y - self._scl(2))), 1)
        pygame.draw.circle(surface, self.outline_color, 
                       (int(self.x + self._scl(1)), int(self.y - self._scl(2))), 1)

        # Draw neck
        pygame.draw.line(surface, self.body_color, 
                     (self.x - self._scl(3), self.y), 
                     (self.x + self._scl(2), self.y), 1)

        # Draw body
        pygame.draw.rect(surface, self.body_color, 
                     (self.x - self._scl(8), self.y, 
                      self._scl(15), self._scl(6)))
        pygame.draw.rect(surface, self.body_color, 
                     (self.x - self._scl(6), self.y + self._scl(6), 
                      self._scl(11), self._scl(5)))
        # Draw neck (horizontal line)
        pygame.draw.line(surface, self.body_color, 
                        (self.x - self._scl(3), self.y + self._scl(1)), 
                        (self.x + self._scl(2), self.y + self._scl(1)), 1)

        # Draw body (two rectangles)
        pygame.draw.rect(surface, self.body_color, 
                        (self.x - self._scl(8), self.y + self._scl(2), 
                         self._scl(15), self._scl(6)))
        pygame.draw.rect(surface, self.body_color, 
                        (self.x - self._scl(6), self.y + self._scl(8), 
                         self._scl(11), self._scl(5)))

        # Draw legs (series of half-circles)
        for i in range(5):
            # Left leg arc
            pygame.draw.arc(surface, self.body_color, 
                           (self.x + self._scl(-6 + i - 0.1) - self._scl(10), 
                            self.y + self._scl(15) - self._scl(10), 
                            self._scl(20), self._scl(20)), 
                           15 * math.pi / 8, math.pi / 4, self._scl(1))
            # Right leg arc
            pygame.draw.arc(surface, self.body_color, 
                           (self.x + self._scl(i) - self._scl(10), 
                            self.y + self._scl(15) - self._scl(10), 
                            self._scl(20), self._scl(20)), 
                           3 * math.pi / 4, 9 * math.pi / 8, self._scl(1))

        # Draw chest (two semi-circles)
        pygame.draw.arc(surface, self.outline_color, 
                       (self.x - self._scl(4.9) - self._scl(4.9), 
                        self.y + self._scl(5) - self._scl(4.9), 
                        self._scl(9.8), self._scl(9.8)), 
                       3 * math.pi / 2, 0, 1)
        pygame.draw.arc(surface, self.outline_color, 
                       (self.x + self._scl(4.9) - self._scl(4.9), 
                        self.y + self._scl(5) - self._scl(4.9), 
                        self._scl(9.8), self._scl(9.8)), 
                       math.pi, 3 * math.pi / 2, 1)

        # Draw arms based on arms_state
        for i in range(-5, 0):
            if self.arms_state == self.RIGHT_UP:
                # Right arm up
                pygame.draw.arc(surface, self.body_color, 
                               (self.x + self._scl(i - 0.1) - self._scl(9), 
                                self.y + self._scl(5) - self._scl(9), 
                                self._scl(18), self._scl(18)), 
                               3 * math.pi / 4, 5 * math.pi / 4, self._scl(1))
                pygame.draw.arc(surface, self.body_color, 
                               (self.x + self._scl(4.9 + i) - self._scl(9), 
                                self.y - self._scl(5) - self._scl(9), 
                                self._scl(18), self._scl(18)), 
                               7 * math.pi / 4, math.pi / 4, self._scl(1))
            elif self.arms_state == self.LEFT_UP:
                # Left arm up
                pygame.draw.arc(surface, self.body_color, 
                               (self.x + self._scl(i - 0.1) - self._scl(9), 
                                self.y - self._scl(5) - self._scl(9), 
                                self._scl(18), self._scl(18)), 
                               3 * math.pi / 4, 5 * math.pi / 4, self._scl(1))
                pygame.draw.arc(surface, self.body_color, 
                               (self.x + self._scl(4.9 + i) - self._scl(9), 
                                self.y + self._scl(5) - self._scl(9), 
                                self._scl(18), self._scl(18)), 
                               7 * math.pi / 4, math.pi / 4, self._scl(1))
            elif self.arms_state == self.ARMS_DOWN:
                # Both arms down
                pygame.draw.arc(surface, self.body_color, 
                               (self.x + self._scl(i - 0.1) - self._scl(9), 
                                self.y + self._scl(5) - self._scl(9), 
                                self._scl(18), self._scl(18)), 
                               3 * math.pi / 4, 5 * math.pi / 4, self._scl(1))
                pygame.draw.arc(surface, self.body_color, 
                               (self.x + self._scl(4.9 + i) - self._scl(9), 
                                self.y + self._scl(5) - self._scl(9), 
                                self._scl(18), self._scl(18)), 
                               7 * math.pi / 4, math.pi / 4, self._scl(1))

    def set_arms_state(self, new_state: int) -> None:
        """
        Updates the arms state (1 = RIGHT_UP, 2 = LEFT_UP, 3 = ARMS_DOWN).
        
        :param new_state: The new arms state to set.
        """
        self.arms_state = new_state
