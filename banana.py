#!/usr/bin/env python
"""
Banana class for the Gorilla game.
Manages position, velocity, angle, drawing, flight updates, and collision detection.
"""

import math
import pygame
from graphics import Graphics
from utils import meters_to_pixels, kmph_to_pixels_per_sec, SKY_COLOR, BANANA_COLOR, SUN_COLOR

class Banana:
    """
    Represents a flying banana with position, velocity, angle, and wind/gravity effects.
    """

    def __init__(
        self,
        x: float,
        y: float,
        angle_deg: float,
        velocity_kmph: float,
        gravity_mps2: float = 9.8,
        wind_mps2: float = 0,
        rpm: float = 200.0,
        graphics=None
    ):
        self.x = x
        self.y = y
        self.angle_deg = angle_deg
        self.rpm = rpm
        self.graphics = graphics

        # Convert real-world units to pixels
        gravity_px = meters_to_pixels(gravity_mps2)
        wind_px = meters_to_pixels(wind_mps2)
        velocity_px = kmph_to_pixels_per_sec(velocity_kmph)

        self.angle_rad = math.radians(angle_deg)

        # Velocity components
        self.vx = math.cos(self.angle_rad) * velocity_px
        self.vy = -math.sin(self.angle_rad) * velocity_px

        self.gravity = gravity_px
        self.wind = wind_px

        self.alive = True
        self.dt_acc = 0.0

    def update(self, dt: float, screen_width: int, screen_height: int) -> None:
        if not self.alive:
            return

        self.dt_acc += dt

        self.vx += self.wind * dt
        self.x += self.vx * dt

        self.y += self.vy * dt
        self.vy += self.gravity * dt

        if self.x < 0 or self.x > screen_width or self.y > screen_height:
            self.alive = False

    def draw(self, screen, orientation=None):
        if not self.alive:
            return

        states_per_second = 4 * (self.rpm / 60.0)
        rotation_index = int(self.dt_acc * states_per_second) % 4

        directions = ["banana_left", "banana_up", "banana_right", "banana_down"]
        selected_orientation = directions[rotation_index]

        self.graphics.draw_banana(self.x, self.y, selected_orientation)

    def XXcheck_collision(self, screen: pygame.Surface, collision_objects: list[dict]) -> str:
        """
        Flexible collision detection using collision objects dict list.

        :param screen: Game screen surface.
        :param collision_objects: List of dictionaries defining collision targets.
        :return: The collided object's name, or "none".
        """
        check_x = int(self.x)
        check_y = int(self.y)

        screen_width, screen_height = screen.get_size()
        #if check_x <= 0 or check_x >= screen_width or check_y >= screen_height:
        if check_x <= 0 or check_x >= screen_width or check_y <= 0 or check_y >= screen_height:
            self.alive = False
            return "boundary"

        color_at_pos = screen.get_at((check_x, check_y))[:3]

        for obj in collision_objects:
            rect = obj.get("rect")
            color = obj.get("color")
            name = obj.get("name", "unknown")

            if rect.collidepoint(check_x, check_y):
                if color:
                    if color_at_pos == color:
                        return name
                else:
                    return name

        if color_at_pos not in (SKY_COLOR, BANANA_COLOR, SUN_COLOR):
            return "building"

        return "none"

    def check_collision(self, collision_objects: list[dict]) -> str:
        """
        Simplified and reliable collision detection using rect-only collision.

        :param collision_objects: List of dictionaries defining collision targets.
        :return: The collided object's name, or "none".
        """
        check_point = pygame.math.Vector2(self.x, self.y)

        for obj in collision_objects:
            rect = obj.get("rect")
            name = obj.get("name", "unknown")

            if rect.collidepoint(check_point):
                return name

        # Boundary checking as fallback
        if not pygame.display.get_surface().get_rect().collidepoint(check_point):
            #self.alive = False
            return "boundary"

        return "none"
