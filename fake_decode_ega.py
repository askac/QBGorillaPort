#!/usr/bin/env python
import pygame
import struct

from graphics import Graphics
from graphics import decode_ega as decodeEga

# EGA palette (16 colors)
EGA_PALETTE = [
    (0,0,0),       # 0 black
    (0,0,170),     # 1 blue
    (0,170,0),     # 2 green
    (0,170,170),   # 3 cyan
    (170,0,0),     # 4 red
    (170,0,170),   # 5 magenta
    (170,85,0),    # 6 brown
    (170,170,170), # 7 gray
    (85,85,85),    # 8 dark gray
    (85,85,255),   # 9 bright blue
    (85,255,85),   # 10 bright green
    (85,255,255),  # 11 bright cyan
    (255,85,85),   # 12 bright red
    (255,85,255),  # 13 bright magenta
    (255,255,85),  # 14 bright yellow
    (255,255,255), # 15 white
]

# EGA banana data from GORILLA.bas
banana_ega_data = {
    "Left": [
        458758,
        202116096,471604224,943208448,943208448,
        943208448,471604224,202116096,0
    ],
    "Down": [
        262153, 
        -2134835200, -2134802239, -2130771968, -2130738945,
        8323072, 8323199, 4063232, 4063294
    ],
    "Up": [
        262153, 
        4063232, 4063294, 8323072, 8323199,
        -2130771968, -2130738945, -2134835200, -2134802239
    ],
    "Right": [
        458758, 
        -1061109760, -522133504, 1886416896, 1886416896,
        1886416896, -522133504, -1061109760, 0
    ]
}

# 可能的 (width, height) 組合
dim_candidates = [
    (6,7),
    (9,4),
    (3,24),
    (4,18),
    (6,12),
    (8,9),
    (9,8),
    (12,6),
    (18,6),
]

HALF_BYTE_LUT = [
    0x0,  # 0000 -> 0000 (0)
    0x8,  # 0001 -> 1000 (8)
    0x4,  # 0010 -> 0100 (4)
    0xC,  # 0011 -> 1100 (12)
    0x2,  # 0100 -> 0010 (2)
    0xA,  # 0101 -> 1010 (10)
    0x6,  # 0110 -> 0110 (6)
    0xE,  # 0111 -> 1110 (14)
    0x1,  # 1000 -> 0001 (1)
    0x9,  # 1001 -> 1001 (9)
    0x5,  # 1010 -> 0101 (5)
    0xD,  # 1011 -> 1101 (13)
    0x3,  # 1100 -> 0011 (3)
    0xB,  # 1101 -> 1011 (11)
    0x7,  # 1110 -> 0111 (7)
    0xF   # 1111 -> 1111 (15)
]

def invert_byte(byte):
    byte = byte & 0xFF
    high_nibble = (byte >> 4) & 0x0F  # 取高4位
    low_nibble = byte & 0x0F         # 取低4位
    return (HALF_BYTE_LUT[low_nibble] << 4) | HALF_BYTE_LUT[high_nibble]

def invert_32bits_fast(value):
    value = value & 0xFFFFFFFF
    byte0 = value & 0xFF
    byte1 = (value >> 8) & 0xFF
    byte2 = (value >> 16) & 0xFF
    byte3 = (value >> 24) & 0xFF
    result = (
        ((HALF_BYTE_LUT[byte3 & 0xF] << 4) | HALF_BYTE_LUT[byte3 >> 4]) << 24 |
        ((HALF_BYTE_LUT[byte2 & 0xF] << 4) | HALF_BYTE_LUT[byte2 >> 4]) << 16 |
        ((HALF_BYTE_LUT[byte1 & 0xF] << 4) | HALF_BYTE_LUT[byte1 >> 4]) << 8 |
        ((HALF_BYTE_LUT[byte0 & 0xF] << 4) | HALF_BYTE_LUT[byte0 >> 4])
    )    
    return result


def decode_ega(data_list) -> pygame.Surface:
    bytes_le = data_list[0].to_bytes(4, byteorder='little', signed=False)
    width, height = struct.unpack('<HH', bytes_le)    
    print(f"Detected {width}x{height}")
    print(f"Max pixels {8*(len(data_list)-1)}")
    max_pixels = 8*(len(data_list)-1)
    total_pixels = width * height

    pwidth = 8 * ((width + 7) // 8) # ceil(a/b) = (a + b - 1) // b
    lines = max_pixels // pwidth
    print(f"PixelPerLins={pwidth}, TotalLines={lines}")

    import math
    import pygame

    if total_pixels > 8*(len(data_list)-1):
        surf = pygame.Surface((width, height))
        surf.fill((255,0,255))  # bright magenta => invalid
        return surf

    combined_bits = 0
    totalBits=0
    for i in range(1,len(data_list)):
        val_32u=invert_32bits_fast(data_list[i] & 0xffffffff)
        combined_bits |= val_32u << totalBits
        totalBits = totalBits + 32

    for x in range(max_pixels*4):
        b0 = 1 if (combined_bits & (1 << x)) else 0
        print(f'{b0}',end="")
        if((x%(pwidth*4))==((pwidth*4)-1)):
            print("")

    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    surf.fill((0,0,0,255))  #Fill blank, opacity

    print(f"pixels_per_line={pwidth} width={width}")
    for i in range(total_pixels):
        x = i % width
        y = i // width
        pi = x + 4*pwidth*y
        p0 = 1 if (combined_bits & (1 << pi)) else 0
        p1 = 1 if (combined_bits & (1 << (pi + pwidth))) else 0
        p2 = 1 if (combined_bits & (1 << (pi + pwidth*2))) else 0
        p3 = 1 if (combined_bits & (1 << (pi + pwidth*3))) else 0
        color_index = (p0 << 0) | (p1 << 1) | (p2 << 2) | (p3 << 3)
        col = EGA_PALETTE[color_index]
        surf.set_at((x,y), col + (255,))

    return surf

def main():
    pygame.init()
    pygame.display.set_caption("EGA Banana Decode Test (Scaled)")

    # 參數：放大倍數
    SCALE = 4

    # 計算要多少視窗大小
    # 假設每張圖寬度最多 16 px、放大 4倍 => 64 px，再加點間隔
    screen_width = 1200
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height))

    graphics = Graphics(screen)

    font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()

    # decode 結果
    banana_surfaces = {}
    orientations = list(banana_ega_data.keys())  # ["Left","Down","Up","Right"]
    for orient in orientations:
        data_list = banana_ega_data[orient]
        for dims in dim_candidates:
            surf = decodeEga(data_list)#decode_ega(data_list)
            w = surf.get_width()
            h = surf.get_height()
            # 產生放大後版本
            big_surf = pygame.transform.scale(surf, (w*SCALE, h*SCALE))
            banana_surfaces[(orient, dims)] = big_surf

    running = True
    while running:
        dt = clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((80,80,120))

        # 顯示欄名
        for c, dims in enumerate(dim_candidates):
            label = f"{dims[0]}x{dims[1]}"
            txt_surf = font.render(label, True, (255,255,255))
            screen.blit(txt_surf, (c*150 + 100, 20))

        # 顯示列名
        for r, orient in enumerate(orientations):
            txt_surf = font.render(orient, True, (255,255,255))
            screen.blit(txt_surf, (20, r*150 + 70))

        # 顯示圖片
        for r, orient in enumerate(orientations):
            for c, dims in enumerate(dim_candidates):
                big_surf = banana_surfaces[(orient, dims)]
                x_draw = c*150 + 100
                y_draw = r*150 + 70
                screen.blit(big_surf, (x_draw, y_draw))

        #graphics.draw_banana(100, 100, "banana_left")

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
