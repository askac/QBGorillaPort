#!/usr/bin/env python
"""
Handles cityscape generation for the Gorilla game.
Generates random buildings with windows.
"""

import random
import pygame

#!/usr/bin/env python
"""
Example Building class for CityScape, with a precomputed "window_map"
to avoid flickering windows.
"""

import random
import pygame

class Building:
    """
    Represents a single building in the cityscape, with optional windows.
    Window "lights" are determined once at initialization to avoid flickering.
    """

    def __init__(self, x: int, width: int, height: int, color: tuple, screen_height: int):
        """
        :param x: The x-coordinate of the building (left edge).
        :param width: The width of the building.
        :param height: The height of the building.
        :param color: The RGB color of the building.
        :param screen_height: Height of the screen (used for positioning).
        """
        # Building position & size
        self.x = x
        self.width = width
        self.height = height
        self.color = color

        # Screen info
        self.screen_height = screen_height

        # Ground is assumed to be 50px from bottom, so the building's top-left Y is:
        self.building_top = self.screen_height - self.height - 50

        # Windows setup
        self.has_windows = True #random.choice([True, False])  # 50% chance to have windows
        self.window_color_lit = (255, 255, 200)  # Light yellow for lit window
        self.window_color_dark = (30, 30, 30)    # Dark color (unlit window)

        # Window size and spacing
        self.window_width = 6
        self.window_height = 10
        self.window_spacing_x = 10
        self.window_spacing_y = 15
        self.litePercent = 0.75

        # Pre-generate the "on/off" map for each window so they won't flicker
        self.window_map = []
        if self.has_windows:
            self._generate_window_map()

    def _generate_window_map(self):
        """
        Randomly determines whether each window in this building is lit or dark,
        and stores the result in a 2D list self.window_map.
        """
        # We'll store windows by columns (x) and rows (y).
        column_list = []
        # Each column is at positions in range(self.x+5, self.x+self.width-...)
        for wx in range(self.x + 5, self.x + self.width - self.window_width, self.window_spacing_x):
            row_list = []
            # Each row is at positions from building_top+5 downward
            for wy in range(self.building_top + 5,
                            self.building_top + self.height - self.window_height,
                            self.window_spacing_y):
                # Decide once if this window is lit
                lit = (random.random() <= self.litePercent)
                row_list.append(lit)
            column_list.append(row_list)
        self.window_map = column_list

    def draw(self, screen: pygame.Surface):
        """
        Draws the building and its windows.
        :param screen: Pygame surface on which to draw.
        """
        # 1) Draw the main building rectangle
        pygame.draw.rect(screen, self.color, (self.x, self.building_top, self.width, self.height))

        # 2) Draw the windows if this building has them
        if self.has_windows:
            self._draw_windows(screen)

    def _draw_windows(self, screen: pygame.Surface):
        """
        Draws windows according to self.window_map. No new random calls here,
        so the pattern won't flicker each frame.
        """
        # We'll iterate over the same columns & rows as in _generate_window_map()
        x_index = 0
        for wx in range(self.x + 5, self.x + self.width - self.window_width, self.window_spacing_x):
            if x_index >= len(self.window_map):
                break

            row_list = self.window_map[x_index]
            y_index = 0
            for wy in range(self.building_top + 5,
                            self.building_top + self.height - self.window_height,
                            self.window_spacing_y):
                if y_index >= len(row_list):
                    break

                # If True => lit, else => dark
                if row_list[y_index]:
                    color = self.window_color_lit
                else:
                    color = self.window_color_dark

                pygame.draw.rect(screen, color, (wx, wy, self.window_width, self.window_height))
                y_index += 1

            x_index += 1

class CityScape:
    """
    Generates and manages a skyline of buildings.
    """

    def __init__(self, screen_width: int, screen_height: int, num_buildings: int = 10):
        """
        :param screen_width: Width of the game screen.
        :param screen_height: Height of the game screen.
        :param num_buildings: Number of buildings to generate.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.num_buildings = num_buildings
        self.buildings = []

        self.generate_buildings()

    def generate_buildings(self):
        self.buildings = []
        min_width = self.screen_width // (self.num_buildings + 2)
        max_width = int(min_width * 1.5)
        ground_level = self.screen_height - 50

        x = 0
        for i in range(self.num_buildings):
            # 1) Random building width
            width = random.randint(min_width, max_width)

            # 2) 如果當前這棟預計會超出螢幕，就調整它的 width
            # 只要還有空間 (x < screen_width)，就把它壓到剛好填滿剩餘的寬度
            if x + width > self.screen_width:
                width = self.screen_width - x
                if width < 10:  # 給個安全值，不讓最後一棟小於 10px
                    break

            # 3) Random building height
            height = random.randint(ground_level // 3, ground_level - 80)
            color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))

            self.buildings.append(Building(x, width, height, color, self.screen_height))

            x += width + random.randint(2, 5)

            # 4) 若超出螢幕，就結束
            if x >= self.screen_width:
                break


    def draw(self, screen: pygame.Surface):
        """
        Draws the cityscape on the given Pygame screen.
        :param screen: The surface to draw on.
        """
        ground_color = (50, 50, 50)
        pygame.draw.rect(screen, ground_color, (0, self.screen_height - 50, self.screen_width, 50))  # Ground

        for building in self.buildings:
            building.draw(screen)  # Each building handles its own drawing
    
    def get_building_positions(self):
        """
        Returns the positions of buildings for collision detection or object placement.
        :return: A list of tuples (x, y, width, height).
        """
        return [(b.x, self.screen_height - b.height - 50, b.width, b.height) for b in self.buildings]
