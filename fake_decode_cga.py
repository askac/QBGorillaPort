#!/usr/bin/env python
import pygame

# 原始 GORILLA.bas 的 CGA 版本香蕉資料
# 依照註解順序：
#  BananaLeft
#  BananaDown
#  BananaUp
#  BananaRight
banana_cga_data = {
    "Left":   [327686, -252645316, 60],
    "Down":   [196618, -1057030081, 49344],
    "Up":     [196618, -1056980800, 63],
    "Right":  [327686, 1010580720, 240],
}

# 要嘗試的寬高 (width x height)
# 你可以加入更多組合，如 (4,8), (8,4) 等，或調整順序
dim_candidates = [
    (8, 4),
    (4, 16),
    (8, 8),
    (8,16),
    (16,8),
    (16,16),
]

def decode_cga_banana(data_list, width=8, height=8) -> pygame.Surface:
    """
    嘗試將 QBasic CGA PUT 資料解出一張 width x height 圖。
    做法：把 data_list (3個int32) 併成 96 bits，
         逐 bit 按 row-major 方式繪製。
    bit=1 => 黃色像素, bit=0 => 透明。
    若你想改用 column-major, 或先讀高位元，也可調整程式。
    """
    # 建立一個透明的 surface
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))

    banana_color = (255, 255, 0, 255)

    # 將 data_list 內的 int (可能有負數) 轉成 96 bits
    combined_bits = 0
    for i, val in enumerate(data_list):
        val_32u = val & 0xFFFFFFFF  # 變為 32-bit 無符號
        # 依序排進 combined_bits：第 i 個 int 往左 shift 32 * i
        combined_bits |= (val_32u << (32 * i))

    # 假設直接 row-major：從 bit 0 開始 → (x=0,y=0) → (x=1,y=0) ... (x=width-1,y=0) → (x=0,y=1)
    bit_idx = 0
    for py in range(height):
        for px in range(width):
            mask = 1 << bit_idx
            pixel_on = (combined_bits & mask) != 0
            if pixel_on:
                surf.set_at((px, py), banana_color)
            bit_idx += 1

    return surf

def main():
    pygame.init()
    pygame.display.set_caption("CGA Banana Decode Test")

    # 設定視窗大小
    # 我們要顯示 4 種方向 × 4 種維度 => 16 張圖片
    # 考量每張可能到 16x16，再加上文字標籤空間
    screen_width = 900
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    SCALE = 4

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    # 事先解碼並存好所有 Surface
    # bananas[(orientation, (w,h))] = surface
    bananas = {}
    orientations = list(banana_cga_data.keys())  # ["Left","Down","Up","Right"]

    for orient in orientations:
        data_list = banana_cga_data[orient]
        for dims in dim_candidates:
            w,h = dims
            surf = decode_cga_banana(data_list, w, h)
            big_surf = pygame.transform.scale(surf, (surf.get_width()*SCALE, surf.get_height()*SCALE))
            bananas[(orient, dims)] = big_surf

    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 清空背景
        screen.fill((60, 60, 90))

        # 顯示標頭 row (列) for orientation, col (行) for dimension
        # 例如 row=0 => "Left", row=1 => "Down", row=2 => "Up", row=3 => "Right"
        # col=0 => "8x8", col=1 => "8x16", col=2 => "16x8", col=3 => "16x16"

        # 設定格子大小
        cell_w = 150  # 每一欄的寬度
        cell_h = 120  # 每一列的高度

        # 在最上方標示各種 dims
        for c, dims in enumerate(dim_candidates):
            label = f"{dims[0]}x{dims[1]}"
            txt_surf = font.render(label, True, (255,255,255))
            # 放置於 (c * cell_w + 20, 10)
            screen.blit(txt_surf, (c*cell_w + 20, 10))

        # 在最左側標示 orientation
        for r, orient in enumerate(orientations):
            txt_surf = font.render(orient, True, (255,255,255))
            # 放置於 (10, r * cell_h + 50)
            screen.blit(txt_surf, (10, r*cell_h + 50))

        # 依序繪製 banana surf
        for r, orient in enumerate(orientations):
            for c, dims in enumerate(dim_candidates):
                x_draw = c * cell_w + 50
                y_draw = r * cell_h + 70
                surf = bananas[(orient, dims)]
                screen.blit(surf, (x_draw, y_draw))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
