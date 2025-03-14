#!/usr/bin/env python
"""
Utility functions for the Gorilla game (modern version without CGA/EGA considerations).
"""

import time
import random
import math

"""
constants.py - Defines global constants for colors and game settings.
"""

# EGA palette (Original from QB Gorilla)
EGA_COLORS = {
    'BLACK': (0, 0, 0),
    'BLUE': (0, 0, 170),
    'GREEN': (0, 170, 0),
    'CYAN': (0, 170, 170),
    'RED': (170, 0, 0),
    'MAGENTA': (170, 0, 170),
    'BROWN': (170, 85, 0),
    'GRAY': (170, 170, 170),
    'DARK_GRAY': (85, 85, 85),
    'BRIGHT_BLUE': (85, 85, 255),
    'BRIGHT_GREEN': (85, 255, 85),
    'BRIGHT_CYAN': (85, 255, 255),
    'BRIGHT_RED': (255, 85, 85),
    'BRIGHT_MAGENTA': (255, 85, 255),
    'BRIGHT_YELLOW': (255, 255, 85),
    'WHITE': (255, 255, 255),
}

# Color constants used in the game
SKY_COLOR = EGA_COLORS['BLUE']
BUILDING_COLORS = [
    EGA_COLORS['CYAN'],
    EGA_COLORS['RED'], 
    EGA_COLORS['MAGENTA'], 
    EGA_COLORS['BROWN']
]
GORILLA_COLOR = EGA_COLORS['BROWN']
BANANA_COLOR = EGA_COLORS['BRIGHT_YELLOW']
EXPLOSION_COLOR = EGA_COLORS['GREEN']
SUN_COLOR = EGA_COLORS['BRIGHT_YELLOW']
GROUND_COLOR = EGA_COLORS['GRAY']
WINDOW_COLOR_LIT = EGA_COLORS['BRIGHT_YELLOW']
WINDOW_COLOR_DARK = EGA_COLORS['DARK_GRAY']

# unit conversion constants
PIXELS_PER_METER = 30  # Adjust this as needed

def meters_to_pixels(m: float) -> float:
    """Converts meters to pixels."""
    return m * PIXELS_PER_METER

def kmph_to_mps(kmph: float) -> float:
    """Converts velocity from kilometers per hour (km/h) to meters per second (m/s)."""
    return kmph * (1000 / 3600)

def kmph_to_pixels_per_sec(kmph: float) -> float:
    """Converts velocity from kilometers per hour (km/h) to pixels per second."""
    mps = kmph_to_mps(kmph)
    return meters_to_pixels(mps)

def scl(n: float) -> int:
    """
    Simplified scale function. No more CGA/EGA checks are needed.
    Just round to the nearest integer.
    
    :param n: The number to be scaled.
    :return: The integer-rounded value of n.
    """
    return int(round(n))

def rest(t: float, speed_const: int = 500, mach_speed: float = 1.0) -> None:
    """
    Pauses the program execution for a given time, adjusted by speed factors.
    
    :param t: Time duration to pause in "game-time" seconds.
    :param speed_const: Speed constant for adjusting game speed.
    :param mach_speed: Machine speed adjustment factor, calculated at startup if needed.
    """
    adjusted_time = (mach_speed * t) / speed_const
    time.sleep(adjusted_time)

def fn_ran(x: int) -> int:
    """
    Match QB
    """
    return int(random.random() * x) + 1

def calc_delay() -> float:
    """
    Measures system speed for timing adjustments, returning a computed delay factor.
    
    :return: A float representing the system's approximate operation speed.
    """
    start_time = time.time()
    counter = 0
    # Count as many increments as possible in 0.5 seconds
    while time.time() - start_time < 0.5:
        counter += 1
    return float(counter)
