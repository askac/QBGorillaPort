#!/usr/bin/env python
"""
Handles graphical rendering for the Gorilla game (banana with 4 orientations using shape drawing).
"""

import math
import pygame
import struct

banana_ega_data = {
    "Left": [
        458758,
        202116096,471604224,943208448,943208448,
        943208448,471604224,202116096,0
    ],
    "Up": [
        262153,
        4063232, 4063294, 8323072, 8323199,
        -2130771968, -2130738945, -2134835200, -2134802239
    ],
    "Down": [
        262153,
        -2134835200, -2134802239, -2130771968, -2130738945,
        8323072, 8323199, 4063232, 4063294
    ],
    "Right": [
        458758,
        -1061109760, -522133504, 1886416896, 1886416896,
        1886416896, -522133504, -1061109760, 0
    ]
}

EGA_PALETTE = [
    (0, 0, 0),
    (0, 0, 170),
    (0, 170, 0),
    (0, 170, 170),
    (170, 0, 0),
    (170, 0, 170),
    (170, 85, 0),
    (170, 170, 170),
    (85, 85, 85),
    (85, 85, 255),
    (85, 255, 85),
    (85, 255, 255),
    (255, 85, 85),
    (255, 85, 255),
    (255, 255, 85),
    (255, 255, 255),
]

# Nibble flip lookup table used in fake_decode_ega.py
HALF_BYTE_LUT = [
    0x0,  # 0000 -> 0000
    0x8,  # 0001 -> 1000
    0x4,  # 0010 -> 0100
    0xC,  # 0011 -> 1100
    0x2,  # 0100 -> 0010
    0xA,  # 0101 -> 1010
    0x6,  # 0110 -> 0110
    0xE,  # 0111 -> 1110
    0x1,  # 1000 -> 0001
    0x9,  # 1001 -> 1001
    0x5,  # 1010 -> 0101
    0xD,  # 1011 -> 1101
    0x3,  # 1100 -> 0011
    0xB,  # 1101 -> 1011
    0x7,  # 1110 -> 0111
    0xF   # 1111 -> 1111
]

def invert_32bits_fast(value: int) -> int:
    """
    This function flips the nibbles of a 32-bit integer, matching the approach 
    in fake_decode_ega.py. Each half-byte (4 bits) is reversed using HALF_BYTE_LUT.
    """
    value &= 0xFFFFFFFF
    b0 = value & 0xFF
    b1 = (value >> 8) & 0xFF
    b2 = (value >> 16) & 0xFF
    b3 = (value >> 24) & 0xFF

    # Perform nibble flipping for each byte
    nb0 = ((HALF_BYTE_LUT[b0 & 0xF] << 4) | HALF_BYTE_LUT[b0 >> 4])
    nb1 = ((HALF_BYTE_LUT[b1 & 0xF] << 4) | HALF_BYTE_LUT[b1 >> 4])
    nb2 = ((HALF_BYTE_LUT[b2 & 0xF] << 4) | HALF_BYTE_LUT[b2 >> 4])
    nb3 = ((HALF_BYTE_LUT[b3 & 0xF] << 4) | HALF_BYTE_LUT[b3 >> 4])

    # Recombine into a single 32-bit value
    return (nb3 << 24) | (nb2 << 16) | (nb1 << 8) | nb0

def decode_ega(
    data_list: list[int],
    requested_width: int = None,
    requested_height: int = None
) -> pygame.Surface:
    """
    Decodes EGA banana (or similar) data to a pygame.Surface using a 4-plane approach.
    1) The first 32 bits may store width/height in <HH> form, or might be other info 
       depending on how GORILLA.bas arranges its data.
    2) The rest of the integers define EGA bitplanes.
    
    In the original fake_decode_ega.py logic:
      - We interpret data_list[0] as two 16-bit fields (width, height).
      - Then we read the rest as pixel data across 4 planes.
      - Planes are arranged in "pwidth" chunks, each line repeated across 4 planes.

    If your GORILLA data differs, adapt this function accordingly.

    :param data_list: The raw EGA data (list of integers).
    :param requested_width: If not None, override the width from data_list[0].
    :param requested_height: If not None, override the height from data_list[0].
    :return: A pygame.Surface with the decoded image.
    """
    # Extract width and height from the first integer if not provided
    # 'little' byteorder, <HH => 2 unsigned shorts
    first_u32 = data_list[0] & 0xFFFFFFFF
    bytes_le = first_u32.to_bytes(4, byteorder='little', signed=False)
    w, h = struct.unpack('<HH', bytes_le)

    # If user provided explicit width/height, override
    if requested_width is not None:
        w = requested_width
    if requested_height is not None:
        h = requested_height

    # The rest of the data (from index=1 onward) is the pixel planes
    # We compute the total number of bits: 32 * (len(data_list)-1)
    max_pixels = 8 * (len(data_list) - 1)  # Because each 32 bits => 32 *  (8 pixels per plane chunk?), 
                                          # but effectively we handle them in 4-plane blocks.

    total_pixels = w * h
    if total_pixels == 0 or len(data_list) < 2:
        # Return a small placeholder if invalid
        surf = pygame.Surface((1,1), pygame.SRCALPHA)
        surf.fill((255,0,255,255))  # Magenta for debugging
        return surf

    # Calculate how many bytes or bits per line for EGA's 4-plane arrangement.
    # In fake_decode_ega.py, we use pwidth=8*((w+7)//8) to handle alignment to 8-pixel boundary
    pwidth = 8 * ((w + 7) // 8)

    # Combine the integer bits into a single large bitset, flipping nibbles if needed
    combined_bits = 0
    shift_acc = 0
    for i in range(1, len(data_list)):
        val_inverted = invert_32bits_fast(data_list[i])
        combined_bits |= (val_inverted << shift_acc)
        shift_acc += 32

    # Create the output surface
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    surf.fill((0,0,0,0))  # transparent background

    # For each pixel, we figure out which bits belong to that pixel across the 4 planes
    # The code uses x + pwidth*(plane_index) + pwidth*lines*(y) arrangement
    # plane0 => bit offset = pi
    # plane1 => bit offset = pi + pwidth
    # plane2 => pi + 2*pwidth
    # plane3 => pi + 3*pwidth
    for i in range(total_pixels):
        x = i % w
        y = i // w
        # pi is the bit index for plane0
        pi = x + pwidth * y

        p0 = 1 if (combined_bits & (1 << pi)) else 0
        p1 = 1 if (combined_bits & (1 << (pi + pwidth))) else 0
        p2 = 1 if (combined_bits & (1 << (pi + 2 * pwidth))) else 0
        p3 = 1 if (combined_bits & (1 << (pi + 3 * pwidth))) else 0

        color_index = (p0 << 0) | (p1 << 1) | (p2 << 2) | (p3 << 3)
        col = EGA_PALETTE[color_index]
        surf.set_at((x, y), col + (255,))

    return surf

class Graphics:
    """
    Class for handling game graphics (no CGA/EGA modes, only modern screen usage).
    """

    def __init__(self, screen):
        """
        Initialize the graphics module.
        :param screen: The main pygame surface where we draw.
        """
        self.screen = screen
        self.ega_surfaces = {}
        self.banana_color = (255, 255, 0)  # Yellow
        self.outline_color = (0, 0, 0)     # Black

    def add_ega_surface(
        self,
        key: str,
        data_list: list[int],
        requested_width: int = None,
        requested_height: int = None,
        scale_factor: int = 1
    ):
        """
        Decodes an EGA surface from data_list, optionally scales it, and stores it in self.ega_surfaces.
        :param key: A string key to identify this surface (e.g. "banana_left").
        :param data_list: The raw EGA data as a list of integers.
        :param requested_width: Optional override for width.
        :param requested_height: Optional override for height.
        :param scale_factor: How much to scale the resulting surface.
        """
        decoded_surf = decode_ega(data_list, requested_width, requested_height)
        if scale_factor > 1:
            w = decoded_surf.get_width()
            h = decoded_surf.get_height()
            decoded_surf = pygame.transform.scale(decoded_surf, (w * scale_factor, h * scale_factor))
        self.ega_surfaces[key] = decoded_surf

    
    def draw_sun(self, x: int, y: int, happy: bool = True) -> None:
        """
        Draws the sun at a given position using basic shape drawing.
        :param x: X coordinate of sun center
        :param y: Y coordinate of sun center
        :param happy: If True, draws a happy mouth; otherwise draws a shocked mouth.
        """
        radius = 30
        pygame.draw.circle(self.screen, self.banana_color, (x, y), radius)  # Sun as a filled circle
        
        # Simple eyes
        eye_radius = 4
        pygame.draw.circle(self.screen, self.outline_color, (x - 10, y - 10), eye_radius)
        pygame.draw.circle(self.screen, self.outline_color, (x + 10, y - 10), eye_radius)
        
        # Mouth
        if happy:
            # Smile arc
            mouth_rect = pygame.Rect(x - 10, y - 5, 20, 10)
            pygame.draw.arc(self.screen, self.outline_color, mouth_rect, math.pi, 2 * math.pi, 2)
        else:
            # Shocked or "O" shaped mouth
            pygame.draw.ellipse(self.screen, self.outline_color, (x - 5, y, 10, 15), 2)
    
    def draw_banana(self, x: float, y: float, key: str):
        """
        Draws a previously decoded EGA banana (or any EGA surface) at position (x, y).

        :param x: X coordinate for top-left corner.
        :param y: Y coordinate for top-left corner.
        :param key: The dictionary key that identifies which EGA surface to draw.
        """
        surf = self.ega_surfaces.get(key)
        if surf:
            self.screen.blit(surf, (x, y))
