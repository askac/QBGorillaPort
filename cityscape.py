#!/usr/bin/env python3
"""
Generates cityscape for Gorilla game, mimicking the original GORILLA.BAS.
"""

import pygame
from utils import BUILDING_COLORS, WINDOW_COLOR_LIT, WINDOW_COLOR_DARK, fn_ran

class Building:
    """
    Represents a single building with windows.
    """
    def __init__(self, x: int, width: int, height: int, color: tuple, screen_height: int):
        self.x = x
        self.width = width
        self.height = height
        self.color = color
        self.screen_height = screen_height
        self.building_top = self.screen_height - self.height - 50

        # Window dimensions and spacing
        self.window_width = 6
        self.window_height = 10
        self.window_spacing_x = 10
        self.window_spacing_y = 15
        self.window_map = []
        self.generate_windows()

    def generate_windows(self):
        """
        Re-generates window map according to updated building height after explosion.
        Ensures no windows appear in destroyed areas.
        """
        self.window_map.clear()

        # Skip windows if building height too small
        if self.height < self.window_height + 5:
            return

        for wx in range(self.x + 3, self.x + self.width - self.window_width, self.window_spacing_x):
            column = []
            for wy in range(self.building_top + 5, self.screen_height - 50 - self.window_height, self.window_spacing_y):
                if wy < self.building_top + self.height:  # Only generate windows within new height
                    column.append(fn_ran(4) != 1)
            self.window_map.append(column)


    def draw(self, screen: pygame.Surface):
        """
        Draws the building and its windows.
        """
        pygame.draw.rect(screen, self.color, (self.x, self.building_top, self.width, self.height))

        for col_idx, column in enumerate(self.window_map):
            wx = self.x + 3 + col_idx * self.window_spacing_x
            for row_idx, lit in enumerate(column):
                wy = self.building_top + 5 + row_idx * self.window_spacing_y
                color = WINDOW_COLOR_LIT if lit else WINDOW_COLOR_DARK
                pygame.draw.rect(screen, color, (wx, wy, self.window_width, self.window_height))


class CityScape:
    """
    Cityscape generation based on original QB GORILLA.BAS logic.
    """
    def __init__(self, screen_width: int, screen_height: int, num_buildings: int = 10):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.num_buildings = num_buildings
        self.buildings = []
        self.generate_buildings()

    def generate_buildings(self):
        """
        Generates buildings using the original QB logic (slope, randomization, color).
        """
        self.buildings.clear()
        ground_level = self.screen_height - 50
        x = 2
        slope = fn_ran(6)

        # Initial building height based on slope type (original QB logic)
        if slope == 1:
            new_height, height_step = 15, 10       # upward
        elif slope == 2:
            new_height, height_step = 130, -10 #downward
        elif slope in [3, 4, 5]:            # V shape
            new_height, height_step = 15, 10
        else:                              # inverted V
            new_height, height_step = 130, -10

        cur_building = 0
        while x < self.screen_width - 20:
            # Adjust height based on slope type
            if slope == 1:
                new_height += height_step
            elif slope == 2:
                new_height += height_step
            elif slope in [3,4,5]: # V shape
                if x > self.screen_width // 2:
                    new_height -= 2 * height_step
                else:
                    new_height += 2 * height_step
            else:  # inverted V
                if x > self.screen_width // 2:
                    new_height += 2 * height_step
                else:
                    new_height -= 2 * height_step

            # Random building width and height (exactly as in QB)
            b_width = fn_ran(37) + 37
            if x + b_width > self.screen_width:
                b_width = self.screen_width - x - 2

            b_height = fn_ran(120) + new_height
            b_height = max(10, min(b_height, ground_level - 50))

            color_idx = fn_ran(4) - 1  # Original QB random selection from 4 colors
            color = BUILDING_COLORS[color_idx]

            # Append building
            self.buildings.append(Building(x, b_width, b_height, color, self.screen_height))

            x += b_width + 2
            cur_building += 1

    def draw(self, screen: pygame.Surface):
        """
        Draws cityscape onto the screen.
        """
        # Draw ground
        pygame.draw.rect(screen, (50, 50, 50), (0, self.screen_height - 50, self.screen_width, 50))
        # Draw buildings
        for building in self.buildings:
            building.draw(screen)

    def get_building_positions(self):
        """
        Returns building positions for game entity placement.
        """
        return [(b.x, b.building_top, b.width, b.height) for b in self.buildings]
 
    def destroy_building_area(self, impact_x: float, impact_y: float, explosion_radius: int = 30) -> None:
        """
        Destroys building parts within explosion_radius around impact point.

        :param impact_x: X coordinate of impact center.
        :param impact_y: Y coordinate of impact center.
        :param explosion_radius: radius of explosion effect.
        """
        impact_point = pygame.math.Vector2(impact_x, impact_y)

        for building in self.buildings:
            building_rect = pygame.Rect(building.x, building.building_top, building.width, building.height)
            if building_rect.collidepoint(impact_point):
                # Calculate destruction depth
                destruction_depth = (impact_y + explosion_radius) - building.building_top
                building.height = max(0, building.height - int(destruction_depth))
                building.building_top = int(self.screen_height - building.height - 50)
                
                # regenerate window map after modifying building height
                building.generate_windows()

    def update_collision_rects(self):
        """
        Update collision rects after explosion.
        Call this whenever buildings are modified.
        """
        self.collision_rects = []
        for building in self.buildings:
            rect = pygame.Rect(
                building.x,
                building.building_top,
                building.width,
                building.height
            )
            self.collision_rects.append(rect)

     