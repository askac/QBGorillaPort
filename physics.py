#!/usr/bin/env python
"""
Physics calculations for the Gorilla game.
"""

import math

def plot_shot(start_x: float, start_y: float, angle: float, velocity: float, gravity: float, wind: float, screen_width: int) -> list:
    """
    Computes the trajectory of a thrown banana.

    :param start_x: Initial x position.
    :param start_y: Initial y position.
    :param angle: Throwing angle in degrees.
    :param velocity: Initial velocity.
    :param gravity: Gravity constant.
    :param wind: Wind effect.
    :param screen_width: Screen width limit.
    :return: List of (x, y) positions of the trajectory.
    """
    angle_rad = math.radians(angle)
    x_velocity = math.cos(angle_rad) * velocity
    y_velocity = math.sin(angle_rad) * velocity
    trajectory = []
    t = 0

    while True:
        x = start_x + (x_velocity * t) + (0.5 * wind * (t ** 2))
        y = start_y - ((y_velocity * t) - (0.5 * gravity * (t ** 2)))
        
        if x < 0 or x > screen_width or y > start_y:
            break

        trajectory.append((x, y))
        t += 0.1

    return trajectory
