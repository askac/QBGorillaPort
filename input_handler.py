#!/usr/bin/env python
"""
Handles user input for the Gorilla game.
"""

import pygame

class InputHandler:
    """
    Class for handling player inputs.
    """

    def __init__(self):
        self.keys = {}

    def handle_event(self, event):
        """
        Handles keyboard and mouse inputs.

        :param event: Pygame event.
        """
        if event.type == pygame.KEYDOWN:
            self.keys[event.key] = True
        elif event.type == pygame.KEYUP:
            self.keys[event.key] = False

    def is_key_pressed(self, key) -> bool:
        """
        Checks if a key is currently pressed.

        :param key: Pygame key constant.
        :return: True if key is pressed, else False.
        """
        return self.keys.get(key, False)
