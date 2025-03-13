#!/usr/bin/env python
"""
Banana class for the Gorilla game.
Manages position, velocity, angle, drawing, and basic flight updates.
"""

import math
import pygame
from graphics import Graphics

class Banana:
    """
    Represents a flying banana with position, velocity, angle, and wind/gravity effects.
    """

    def __init__(
        self,
        x: float,
        y: float,
        angle_deg: float,
        velocity: float,
        gravity: float,
        wind: float
    ):
        """
        :param x: Initial X position of the banana.
        :param y: Initial Y position of the banana.
        :param angle_deg: Throw angle in degrees.
        :param velocity: Initial throw velocity.
        :param gravity: Gravity constant (e.g., 9.8).
        :param wind: Horizontal wind force.
        """
        self.x = x
        self.y = y
        self.angle_deg = angle_deg
        self.velocity = velocity
        self.gravity = gravity
        self.wind = wind

        # Convert angle to radians
        self.angle_rad = math.radians(angle_deg)

        # Decompose velocity into X / Y components
        self.vx = math.cos(self.angle_rad) * self.velocity
        self.vy = -math.sin(self.angle_rad) * self.velocity  # Negative because screen y+ down

        # Flight state
        self.alive = True   # Banana will disappear when it hits ground or goes out of screen
        self.rotation_step = 0  # Used to choose among the 4 banana orientations
        self.dt_acc = 0.0      # Accumulated time used for flight

        # For drawing the banana; we can reuse the Graphics class
        # Typically, in a bigger architecture, we'd have a shared `Graphics` or
        # we'd pass screen around. Here, let's store an instance or accept it in draw().
        self.graphics = None  # We'll set it externally or handle in draw()

    def update(self, dt: float, screen_width: int, screen_height: int) -> None:
        """
        Updates the banana's position based on velocity, wind, and gravity.

        :param dt: Time elapsed (seconds) since last frame/update.
        :param screen_width: For boundary checking (width).
        :param screen_height: For boundary checking (height).
        """
        if not self.alive:
            return

        # Accumulate time for simpler banana orientation changes
        self.dt_acc += dt

        # Horizontal motion includes wind
        # wind can be seen as an additional constant acceleration
        # (like "ax = wind"), or a scaled effect; here's a basic approach:
        # self.x += self.vx * dt + 0.5 * wind * (dt^2)
        # But for simplicity, we'll just treat wind as a small horizontal acceleration:
        self.vx += self.wind * dt
        self.x += self.vx * dt

        # Vertical motion includes gravity
        # vy(t+dt) = vy(t) + gravity * dt
        # y(t+dt) = y(t) + vy(t)*dt + 0.5*g*(dt^2)
        # We'll do a simpler approach: y += vy*dt, then vy += g*dt
        self.y += self.vy * dt
        self.vy += self.gravity * dt  # gravity is positive if y goes down screen

        # Check if out of screen or "hit the ground"
        # If we want the ground to be screen_height-50, we can adapt accordingly.
        if self.x < 0 or self.x > screen_width or self.y > screen_height:
            self.alive = False

    def draw(self, screen, graphics, orientation=None):
        """
        Draws the banana using the Graphics module.
        :param screen: The pygame surface to draw on.
        :param graphics: The Graphics instance that handles rendering.
        :param orientation: Optional; specifies EGA banana sprite.
        """
        if not self.alive:
            return

        # Determine orientation index (CGA uses rotation index)
        if orientation is None:
            orientation = self.rotation_step % 4  # Default rotation for CGA
    
        # Draw banana using the graphics system
        graphics.draw_banana(self.x, self.y, orientation)
