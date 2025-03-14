import pygame
import math
from utils import scl

class QBDraw:
    def __init__(self, surface, offset_x=0, offset_y=0, scale=1.0, line_thickness=1, point_size=1, scale_lines=True, scale_points=True):
        """
        Initialize the QBDraw class with scaling options for lines and points.

        Parameters:
        - surface: The Pygame surface to draw on.
        - offset_x (int): X offset for drawing (default 0).
        - offset_y (int): Y offset for drawing (default 0).
        - scale (float): Scaling factor for positions and optionally sizes (default 1.0).
        - line_thickness (int): Base thickness of lines (default 1).
        - point_size (int): Base size of points (default 1).
        - scale_lines (bool): If True, line thickness scales with scale factor (default False).
        - scale_points (bool): If True, point size scales with scale factor (default False).
        """
        self.surface = surface
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.scale = scale
        # Scale line thickness if scale_lines is True, otherwise keep it fixed; ensure at least 1 pixel
        self.line_thickness = max(1, int(line_thickness * scale)) if scale_lines else line_thickness
        self.scale_lines = scale_lines
        # Scale point size if scale_points is True, otherwise keep it fixed; ensure at least 1 pixel
        self.point_size = max(1, int(point_size * scale)) if scale_points else point_size

    def _scale_pos(self, x, y):
        """Scale and offset a position from unscaled units to screen coordinates."""
        return int(self.offset_x + x * self.scale), int(self.offset_y + y * self.scale)

    def LINE(self, x1, y1, x2, y2, color, box=False, fill=False):
        """Draw a line or box with scaling."""
        # Scale the coordinates
        x1, y1 = self._scale_pos(x1, y1)
        x2, y2 = self._scale_pos(x2, y2)

        if box:
            # Determine top-left corner and dimensions
            left = min(x1, x2)
            top = min(y1, y2)
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1

            # Adjust thickness based on scaling option
            thickness = int(self.scale * self.line_thickness) if self.scale_lines else self.line_thickness

            if fill:
                # Filled box (BF), no thickness
                pygame.draw.rect(self.surface, color, (left, top, width, height))
            else:
                # Unfilled box (B), apply thickness
                pygame.draw.rect(self.surface, color, (left, top, width, height), thickness)
        else:
            # Regular line
            #thickness = int(self.scale * self.line_thickness) if self.scale_lines else self.line_thickness
            pygame.draw.line(self.surface, color, (x1, y1), (x2, y2), self.line_thickness)#thickness)
            
    def LINE_OLD(self, x1, y1, x2, y2, color, box=False, fill=True):
        """Draw a line or rectangle with scaling and optional filling."""
        x1, y1 = self._scale_pos(x1, y1)
        x2, y2 = self._scale_pos(x2, y2)
        if box:
            left = min(x1, x2)
            top = min(y1, y2)
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            if fill:
                pygame.draw.rect(self.surface, color, (left, top, width, height))
            else:
                pygame.draw.rect(self.surface, color, (left, top, width, height), self.line_thickness)
        else:
            pygame.draw.line(self.surface, color, (x1, y1), (x2, y2), self.line_thickness)

    def xxCIRCLE(self, x, y, radius, color, start_angle=None, end_angle=None):
        """Draw a circle or arc with scaling and optional angles for arcs."""
        x, y = self._scale_pos(x, y)
        radius = int(radius * self.scale)
        if start_angle is None or end_angle is None:
            pygame.draw.circle(self.surface, color, (x, y), radius, self.line_thickness)
        else:
            rect = (x - radius, y - radius, 2 * radius, 2 * radius)
            # Pygame draws arcs counter-clockwise, so swap and negate angles
            #pygame.draw.arc(self.surface, color, rect, -end_angle, -start_angle, self.line_thickness)
            pygame.draw.arc(self.surface, color, rect, start_angle, end_angle, self.line_thickness)

    def CIRCLE(self, x, y, radius, color, start_angle=None, end_angle=None, fill=False):
        if fill:
            # Filled circle
            pygame.draw.circle(self.surface, color,
                           (self.offset_x + scl(x), self.offset_y + scl(y)),
                           scl(radius), 0)
        else:
            if start_angle is None or end_angle is None:
                # Full circle outline
                pygame.draw.circle(self.surface, color,
                               (self.offset_x + scl(x), self.offset_y + scl(y)), scl(radius), 1)
            else:
                # Arc only
                rect = pygame.Rect(self.offset_x + scl(x - radius), self.offset_y + scl(y - radius),
                               2*scl(radius), 2*scl(radius))
                pygame.draw.arc(self.surface, color, rect, start_angle, end_angle, 1)

    def PSET(self, x, y, color):
        """Set a pixel or draw a small circle for a point with scaling."""
        x, y = self._scale_pos(x, y)
        if self.point_size == 1:
            self.surface.set_at((x, y), color)  # Single pixel
        else:
            pygame.draw.circle(self.surface, color, (x, y), self.point_size)  # Scaled size

