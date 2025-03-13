#!/usr/bin/env python
"""
Utility functions for the Gorilla game (modern version without CGA/EGA considerations).
"""

import time
import random
import math

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
    Returns a random integer in the range [1, x].
    
    :param x: Upper limit for the random number.
    :return: A random integer between 1 and x, inclusive.
    """
    return random.randint(1, x)

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
