以下是一份詳細的移植規劃，目標是將 GORILLA.bas 移植成一個具備現代程式設計指引的 Python 遊戲專案。規劃中將著重於模組化、物件導向設計、事件驅動架構以及現代化的程式風格（如遵循 PEP 8），以利維護與擴展。

---

## 一、專案架構規劃

### 1.1 檔案與模組分離

將專案拆分成數個模組，每個模組負責不同的功能：  
- **main.py**  
  - 負責專案入口，初始化遊戲、設定環境並啟動遊戲主迴圈。
- **game.py**  
  - 包含主要遊戲邏輯，例如遊戲狀態管理（Intro、Playing、Game Over）、回合控制、分數更新等。
- **graphics.py**  
  - 使用現代圖形庫（例如 Pygame）來取代 QBasic 的繪圖命令。  
  - 包含繪製大猩猩、香蕉、城市天際線、爆炸、太陽等圖形函式。
- **sound.py**  
  - 整合音效播放，利用 Pygame 的 mixer 或其他聲音庫來處理原 BASIC 中的 PLAY 指令。
- **physics.py**  
  - 處理拋物線軌跡、重力、風速等物理運算邏輯。
- **input_handler.py**  
  - 管理使用者輸入、鍵盤事件及其他互動事件。
- **utils.py**  
  - 放置共用工具函式，例如 Scl() 數值縮放函式、常數定義、錯誤處理等。

---

## 二、物件導向設計

### 2.1 主要類別規劃

利用類別來封裝遊戲中的各個實體及功能，降低模組間的耦合度與增加擴展性。

- **Game**  
  - 屬性：遊戲狀態、玩家清單、建築物、目前回合等。  
  - 方法：`init()`, `run()`, `update()`, `handle_events()`, `render()` 等。
  
- **Gorilla**  
  - 屬性：位置、圖形資料、分數、狀態（舉手、倒下、爆炸）等。  
  - 方法：`draw()`, `explode()`, `victory_dance()` 等。

- **Banana**  
  - 屬性：起始位置、角度、速度、當前位置、旋轉狀態等。  
  - 方法：`update_position()`, `draw()`, `check_collision()` 等。

- **CityScape**  
  - 屬性：建築物列表、天際線資料等。  
  - 方法：`generate()`, `draw_buildings()` 等。

- **Sun**  
  - 屬性：位置、狀態（正常、被擊中）等。  
  - 方法：`draw()`, `update_state()` 等。

### 2.2 狀態管理

利用狀態機設計模式，管理不同遊戲狀態：  
- **Intro State**：顯示遊戲說明與導入畫面。  
- **Playing State**：進入主遊戲迴圈，依照玩家回合處理拋香蕉、碰撞檢測等。  
- **Game Over State**：顯示最終分數、勝負結果與重新開始選項。

---

## 三、現代程式設計指引

### 3.1 程式碼風格與規範
- **PEP 8**：遵循 Python 的程式碼風格指南，包含命名規則、縮排、註解與空白行使用。
- **Docstrings 與註解**：為每個模組、類別與函式添加清楚的說明，方便維護與團隊協作。
- **型別提示 (Type Hints)**：利用 Python 的型別提示提高程式可讀性與錯誤檢查。

### 3.2 測試與除錯
- 撰寫單元測試 (Unit Test) 來覆蓋核心遊戲邏輯（如物理計算、狀態更新）。
- 使用 logging 模組記錄遊戲運作狀態與錯誤訊息，方便追蹤與除錯。

### 3.3 依賴管理與虛擬環境
- 使用 pipenv 或 poetry 來管理專案依賴，並確保開發環境一致。
- 撰寫 requirements.txt 或 pyproject.toml，明確記錄所需的庫（例如 Pygame）。

### 3.4 事件驅動設計
- 利用 Pygame 提供的事件系統來管理使用者輸入與遊戲更新。  
- 以主遊戲迴圈不斷處理事件、更新狀態並重新繪製畫面。

---

## 四、簡單範例架構 (Python Skeleton)

以下是一個簡單的範例程式架構，說明如何從 main.py 啟動並進入遊戲迴圈：

```python
#!/usr/bin/env python
"""
Main entry point for the Gorilla game ported to Python.
"""

import pygame
from game import Game

def main():
    # Initialize pygame and create game instance
    pygame.init()
    game = Game()
    game.run()  # Start the main game loop

if __name__ == '__main__':
    main()
```

在 **game.py** 中，可以有類似下面的基本架構：

```python
import pygame
from graphics import Graphics
from input_handler import InputHandler
from physics import Physics
from sound import Sound

class Game:
    """
    Main Game class to handle game initialization, loop, and state.
    """
    def __init__(self):
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Gorilla Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize submodules
        self.graphics = Graphics(self.screen)
        self.input_handler = InputHandler()
        self.physics = Physics()
        self.sound = Sound()
        
        # Initialize game entities (gorillas, bananas, cityscape, etc.)
        self.init_game_entities()
    
    def init_game_entities(self):
        # Create Gorilla, CityScape, etc.
        pass
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # Limit to 60 FPS
        pygame.quit()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # 進一步處理鍵盤與滑鼠事件
            self.input_handler.handle_event(event)
    
    def update(self):
        # 更新遊戲邏輯，如香蕉拋物線運算、碰撞檢測、狀態更新等
        pass
    
    def render(self):
        # 清除畫面、重新繪製所有圖形
        self.screen.fill((0, 0, 0))
        self.graphics.draw_all()
        pygame.display.flip()
```

---

## 五、移植策略與步驟

1. **核心邏輯移植**  
   - 將 QBasic 中的物理運算（香蕉軌跡、重力、風速計算）、分數計算及狀態切換邏輯直接轉換為 Python 函式，並撰寫單元測試驗證運算正確性。

2. **圖形與聲音重寫**  
   - 根據 Pygame 的 API 重新設計繪製大猩猩、香蕉、城市天際線及爆炸動畫的函式，轉換 QBasic 的即時繪圖命令到基於 frame 的繪製流程。
   - 音效部分則利用 pygame.mixer 播放事先準備好的音效檔案。

3. **事件處理與使用者輸入**  
   - 使用 Pygame 事件系統取代 INKEY$ 與 LINE INPUT，根據需要設計 GUI 或簡單的文字輸入介面。

4. **重構資料結構**  
   - 以 Python 的 class 來定義 Gorilla、Banana、CityScape 等，將原 BASIC 中的全域變數與動態陣列轉換成物件屬性與列表，提升結構化與可讀性。

5. **整合與測試**  
   - 將各個模組整合進入遊戲主迴圈中，並逐步進行測試，確認遊戲的每個功能模組皆能正確運作。

---

## 六、結論

透過上述規劃，我們可以依照以下步驟完成移植工作：
- 分離核心遊戲邏輯與視覺／音效處理模組。  
- 利用現代物件導向設計重構遊戲結構，並採用事件驅動的主迴圈。  
- 遵循 PEP 8 與使用型別提示、docstrings 等提高程式品質。  
- 撰寫單元測試並使用 logging 輔助除錯。

這樣的架構不僅能有效地將 GORILLA.bas 移植到 Python，還能使專案具備良好的擴充性與維護性，符合現代軟體工程的設計理念。
