#!/usr/bin/env python
"""
Handles sound effects for the Gorilla game.
"""

import pygame

class Sound:
    """
    Sound manager for the game.
    """

    def __init__(self):
        pygame.mixer.init()
        self.throw_sound = pygame.mixer.Sound("sounds/throw.wav")
        self.explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
        self.victory_sound = pygame.mixer.Sound("sounds/victory.wav")

    def play_throw(self):
        """Plays the banana throw sound."""
        self.throw_sound.play()

    def play_explosion(self):
        """Plays the explosion sound."""
        self.explosion_sound.play()

    def play_victory(self):
        """Plays the victory jingle."""
        self.victory_sound.play()
