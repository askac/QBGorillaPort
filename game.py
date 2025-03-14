#!/usr/bin/env python3
"""
Main game logic module for QB Gorilla game port to modern Python.
Now integrates:
1. ThrowController - handle angle/power from keyboard or mouse
2. Multi-message UI support
"""

import pygame
import random
import math
from gorilla import Gorilla
from banana import Banana
from cityscape import CityScape
from graphics import Graphics
from sound import Sound
from utils import SKY_COLOR, GROUND_COLOR, GORILLA_COLOR, SUN_COLOR

# (Paste ThrowController class here if not in a separate file)
from throw_controller import ThrowController  # Example if you made a separate file

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 1280, 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Gorilla Game")

        self.clock = pygame.time.Clock()
        self.running = True

        # Graphics, sound, city init
        self.graphics = Graphics(self.screen)
        try:
            self.sound = Sound()
        except:
            self.sound = None

        self.cityscape = CityScape(self.screen_width, self.screen_height)

        # Gorilla / Banana
        positions = self.cityscape.get_building_positions()
        self.gorilla1 = Gorilla(positions[1][0] + 20, positions[1][1] - 30)
        self.gorilla2 = Gorilla(positions[-2][0] + 20, positions[-2][1] - 30)

        self.banana = None

        # Turn logic
        self.turn = 0

        # Sun
        self.sun_x = self.screen_width // 2
        self.sun_y = 25
        self.sun_happy = True

        # Collision
        self.collision_objects = []
        self._load_collision_objects()
        self._load_collision_buildings()

        # Throw controller
        self.throw_controller = ThrowController()
        # 也可在此切換模式: self.throw_controller.set_input_mode("mouse")

        # For multi-message UI
        self.ui_messages = []  # each item: (text_surface, rect, start_time, duration_ms)

    def _load_collision_objects(self):
        self.collision_objects = [
            {
                "name": "sun",
                "rect": pygame.Rect(self.sun_x - 22, self.sun_y - 18, 44, 36)
            },
            {
                "name": "gorilla1",
                "rect": pygame.Rect(self.gorilla1.x - 15, self.gorilla1.y, 30, 40)
            },
            {
                "name": "gorilla2",
                "rect": pygame.Rect(self.gorilla2.x - 15, self.gorilla2.y, 30, 40)
            }
        ]

    def _load_collision_buildings(self):
        for building in self.cityscape.buildings:
            rect = pygame.Rect(building.x, building.building_top, building.width, building.height)
            self.collision_objects.append({
                "name": "building",
                "rect": rect
            })

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            if not self.handle_events():
                break
            self.update(dt)
            self.render()

        pygame.quit()

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            # Pass to throw_controller
            self.throw_controller.handle_event(event)

            # Example: if releasing SPACE or finishing mouse drag triggers banana throw
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    # finalize banana throw
                    angle, power = self.throw_controller.get_throw_params()
                    if power > 1:  # avoid zero throws
                        self.do_throw(angle, power)
                    self.throw_controller.reset()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.throw_controller.mode == "mouse":
                    angle, power = self.throw_controller.get_throw_params()
                    if power > 1:
                        self.do_throw(angle, power)
                    self.throw_controller.reset()

        return True

    def do_throw(self, angle, power):
        """
        Create a Banana with given angle & power.
        For demonstration, let's treat 'power' as velocity_kmph.
        """
        # Decide which gorilla is throwing
        thrower_x = self.gorilla1.x if self.turn == 0 else self.gorilla2.x
        thrower_y = self.gorilla1.y if self.turn == 0 else self.gorilla2.y


        angle += random.uniform(-5, 5)
        power = 15 + 35 * power // 100 + random.uniform(-5, 5)
        if 0!= (self.screen_width//640):
            power = int(power * math.sqrt(self.screen_width//640))

        # If right gorilla, angle might invert
        final_angle = angle if self.turn == 0 else -angle
        final_power = power if self.turn == 0 else -power
        print(f"final power={final_power}, angle={angle}")

        self.banana = Banana(
            thrower_x, thrower_y,
            final_angle, velocity_kmph=final_power,
            gravity_mps2=9.8, wind_mps2=random.uniform(-2, 2),
            graphics=self.graphics
        )
        # Switch turn
        self.turn = (self.turn + 1) % 2

        # arms up
        if self.turn == 0:
            self.gorilla1.set_arms_state(Gorilla.LEFT_UP)
            self.gorilla2.set_arms_state(Gorilla.ARMS_DOWN)
        else:
            self.gorilla1.set_arms_state(Gorilla.ARMS_DOWN)
            self.gorilla2.set_arms_state(Gorilla.RIGHT_UP)

        if self.sound:
            self.sound.play_throw()

    def update(self, dt: float):
        self.throw_controller.update(dt)

        # Update banana
        if self.banana and self.banana.alive:
            self.banana.update(dt, self.screen_width, self.screen_height)
            collision_result = self.banana.check_collision(self.collision_objects)
            self.sun_happy = True
            if collision_result != "none":
                self.banana.alive = False
                if collision_result == "sun":
                    self.sun_happy = False
                    print("Hit the sun!")
                    self.banana.alive = True
                    # maybe do something else
                elif collision_result == "gorilla1":
                    self.graphics.draw_explosion(self.banana.x, self.banana.y)
                    self.add_ui_message("Gorilla Richard WIN!!", duration_ms=3000)
                    self.gorilla2.victory_dance(self.screen, self.render, self.sound.play_victory if self.sound else None, cycles=5)
                    pygame.time.delay(1000)
                    self.reset()
                elif collision_result == "gorilla2":
                    self.graphics.draw_explosion(self.banana.x, self.banana.y)
                    self.add_ui_message("Gorilla Loki WIN!!", duration_ms=3000)
                    self.gorilla1.victory_dance(self.screen, self.render, self.sound.play_victory if self.sound else None, cycles=5)
                    pygame.time.delay(1000)
                    self.reset()
                elif collision_result == "building":
                    self.graphics.draw_explosion(self.banana.x, self.banana.y)
                    self.cityscape.destroy_building_area(self.banana.x, self.banana.y, 30)
                    print("Banana hit building!")
                    # reload building collision
                    self.collision_objects = [obj for obj in self.collision_objects if obj["name"] != "building"]
                    self._load_collision_buildings()
                    self.snap_gorilla_onto_building()

                elif collision_result == "ground":
                    self.graphics.draw_explosion(self.banana.x, self.banana.y)
                    print("Hit ground!")
                elif collision_result == "boundary":
                    print("Banana off screen")
                    if(self.banana.y <= 0):
                        print("Banana fly high! It will back soon")
                        self.banana.alive = True

                if self.sound and not self.banana.alive:
                    self.sound.play_explosion()
     
        # 更新 UI 訊息 (移除過期)
        current_time = pygame.time.get_ticks()
        self.ui_messages = [
            (surf, rect, st, dur)
            for (surf, rect, st, dur) in self.ui_messages
            if dur <= 0 or (current_time - st) < dur
        ]

    def render(self):
        self.screen.fill(SKY_COLOR)
        pygame.draw.rect(self.screen, GROUND_COLOR, (0, self.screen_height - 50, self.screen_width, 50))
        self.collision_objects.append({"name": "ground", "rect": pygame.Rect(0, self.screen_height - 50, self.screen_width, 50)})

        self.graphics.draw_sun(self.sun_x, self.sun_y, happy=self.sun_happy)
        self.cityscape.draw(self.screen)
        self.gorilla1.draw(self.screen)
        self.gorilla2.draw(self.screen)

        if self.banana and self.banana.alive:
            self.banana.draw(self.screen)

        # 顯示 UI 訊息
        for (surf, rect, start_time, duration) in self.ui_messages:
            self.screen.blit(surf, rect)

        # 顯示角度 / 力量 (for debug)
        angle_text = f"Angle: {int(self.throw_controller.angle)}"
        power_text = f"Power: {int(self.throw_controller.power)} / {int(self.throw_controller.max_power)}"
        player_text = f"Gorilla: Loki" if self.turn == 0 else f"Gorilla: Richard"
        player_text = f"{player_text}  [SPACE]: Charging Power. [UP]/[DOWN]: Adjust Angle"
        font = pygame.font.Font(None, 28)
        angle_surf = font.render(angle_text, True, (255,255,255))
        power_surf = font.render(power_text, True, (255,255,255))
        player_surf = font.render(player_text, True, (255,255,0))
        self.screen.blit(angle_surf, (10, 10))
        self.screen.blit(power_surf, (10, 40))
        self.screen.blit(player_surf, (10, 70))

        pygame.display.flip()

    def add_ui_message(self, text: str, duration_ms: int = 2000, position=None, font_size: int = 48, color=(255,255,255)):
        """
        Adds a message to the screen UI for a set duration. 
        If duration_ms <= 0, means it won't expire automatically.
        """
        if position is None:
            x = self.screen_width // 2
            y = self.screen_height // 2
        else:
            x, y = position

        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect(center=(x,y))
        start_time = pygame.time.get_ticks()
        self.ui_messages.append((text_surface, rect, start_time, duration_ms))

    def reset(self):
        """
        Resets the game round, as in original QB GORILLA.
        """
        self.ui_messages.clear()

        self.cityscape.generate_buildings()
        positions = self.cityscape.get_building_positions()
        self.gorilla1.x, self.gorilla1.y = positions[1][0] + 20, positions[1][1] - 30
        self.gorilla2.x, self.gorilla2.y = positions[-2][0] + 20, positions[-2][1] - 30

        self.gorilla1.set_arms_state(Gorilla.ARMS_DOWN)
        self.gorilla2.set_arms_state(Gorilla.ARMS_DOWN)

        self.banana = None
        self.sun_happy = True

        self._load_collision_objects()
        self._load_collision_buildings()

        self.render()
        pygame.time.delay(1000)

    def snap_gorilla_onto_building(self):
        """
        Moves gorilla downward onto the top of any building that covers gorilla.x horizontally,
        but never moves it upward. If no valid building is found, places gorilla on the ground.

        This prevents the gorilla from "jumping up" due to a taller building's top being higher.
        """

        # Gorilla / Banana
        positions = self.cityscape.get_building_positions()
        self.gorilla1 = Gorilla(positions[1][0] + 20, positions[1][1] - 30)
        self.gorilla2 = Gorilla(positions[-2][0] + 20, positions[-2][1] - 30)
 



def main():
    game = Game()
    # 如果要用滑鼠 => game.throw_controller.set_input_mode("mouse")
    game.run()

if __name__ == '__main__':
    main()
