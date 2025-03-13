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

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the gorilla on the given Pygame surface,
        using geometric shapes and arcs to resemble the original GORILLA.bas design.
        
        :param surface: Pygame surface on which the gorilla should be drawn.
        """
        s = self._scl

        # Head
        head_rect1 = pygame.Rect(self.x + s(-4), self.y + s(0), s(7), s(6))
        pygame.draw.rect(surface, self.body_color, head_rect1)
        pygame.draw.rect(surface, self.outline_color, head_rect1, 1)

        head_rect2 = pygame.Rect(self.x + s(-5), self.y + s(2), s(9), s(2))
        pygame.draw.rect(surface, self.body_color, head_rect2)
        pygame.draw.rect(surface, self.outline_color, head_rect2, 1)

        # Brow line
        brow_start = (self.x + s(-3), self.y + s(2))
        brow_end   = (self.x + s( 2), self.y + s(2))
        pygame.draw.line(surface, self.outline_color, brow_start, brow_end, 1)

        # Nose/eyes
        for offset in range(-2, 0):
            nose_x1 = self.x + s(offset)
            nose_x2 = self.x + s(offset + 3)
            nose_y  = self.y + s(4)
            pygame.draw.circle(surface, self.outline_color, (nose_x1, nose_y), 1)
            pygame.draw.circle(surface, self.outline_color, (nose_x2, nose_y), 1)

        # Neck
        neck_start = (self.x + s(-3), self.y + s(7))
        neck_end   = (self.x + s( 2), self.y + s(7))
        pygame.draw.line(surface, self.body_color, neck_start, neck_end, 2)

        # Body
        body_rect1 = pygame.Rect(self.x + s(-8), self.y + s(8), s(15), s(6))
        pygame.draw.rect(surface, self.body_color, body_rect1)
        pygame.draw.rect(surface, self.outline_color, body_rect1, 1)

        body_rect2 = pygame.Rect(self.x + s(-6), self.y + s(15), s(11), s(5))
        pygame.draw.rect(surface, self.body_color, body_rect2)
        pygame.draw.rect(surface, self.outline_color, body_rect2, 1)

        # Legs
        for i in range(0, 5):
            center_r = (self.x + s(i), self.y + s(25))
            pygame.draw.arc(
                surface,
                self.body_color,
                (center_r[0] - s(10), center_r[1] - s(10), s(20), s(20)),
                3 * math.pi / 4,
                9 * math.pi / 8,
                2
            )
            center_l = (self.x + s(-6 + (i - 0.1)), self.y + s(25))
            pygame.draw.arc(
                surface,
                self.body_color,
                (center_l[0] - s(10), center_l[1] - s(10), s(20), s(20)),
                15 * math.pi / 8,
                math.pi / 4,
                2
            )

        # Arms
        if self.arms_state == self.RIGHT_UP:
            self._draw_arm_arc(surface, offset_x=-0.1, offset_y=14, start_angle=3 * math.pi / 4, end_angle=5 * math.pi / 4)
            self._draw_arm_arc(surface, offset_x=4.9,  offset_y=4,  start_angle=7 * math.pi / 4, end_angle=math.pi / 4)
        elif self.arms_state == self.LEFT_UP:
            self._draw_arm_arc(surface, offset_x=-0.1, offset_y=4,  start_angle=3 * math.pi / 4, end_angle=5 * math.pi / 4)
            self._draw_arm_arc(surface, offset_x=4.9,  offset_y=14, start_angle=7 * math.pi / 4, end_angle=math.pi / 4)
        else:
            # Both arms down
            self._draw_arm_arc(surface, offset_x=-0.1, offset_y=14, start_angle=3 * math.pi / 4, end_angle=5 * math.pi / 4)
            self._draw_arm_arc(surface, offset_x=4.9,  offset_y=14, start_angle=7 * math.pi / 4, end_angle=math.pi / 4)

    def _draw_arm_arc(
        self,
        surface: pygame.Surface,
        offset_x: float,
        offset_y: float,
        start_angle: float,
        end_angle: float
    ) -> None:
        """
        Draws a single arm arc, simulating the original QBasic approach.
        """
        s = self._scl
        cx = self.x + s(offset_x)
        cy = self.y + s(offset_y)
        radius = s(9)
        
        pygame.draw.arc(surface, self.body_color, (cx - radius, cy - radius, radius * 2, radius * 2), start_angle, end_angle, s(2))
        pygame.draw.arc(surface, self.outline_color, (cx - radius, cy - radius, radius * 2, radius * 2), start_angle, end_angle, 1)

    def _scl(self, val: float) -> int:
        """
        Scales a coordinate or size value by the Gorilla's scale factor,
        mimicking the idea of Scl() in the original code.
        """
        return int(round(val * self.scale))


    def set_arms_state(self, new_state: int) -> None:
        """
        Updates the arms state (1 = RIGHT_UP, 2 = LEFT_UP, 3 = ARMS_DOWN).
        
        :param new_state: The new arms state to set.
        """
        self.arms_state = new_state

