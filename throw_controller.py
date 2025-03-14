import pygame
import math

class ThrowController:
    """
    Manages angle and power inputs for throwing bananas.
    Can switch between 'keyboard' mode (hold SPACE to charge) or 'mouse' mode (drag).
    """

    def __init__(self):
        self.angle = 45.0
        self.power = 0.0
        self.max_power = 100.0
        self.angle_min = 10.0
        self.angle_max = 80.0

        # Keyboard charging
        self.charging = False  # True while holding SPACE

        # Mouse drag
        self.mouse_drag = False
        self.drag_start_pos = None
        self.drag_current_pos = None

        # Default mode
        self.mode = "keyboard"  # "keyboard" or "mouse"

    def set_input_mode(self, mode: str):
        """
        Switches input mode: 'keyboard' or 'mouse'
        """
        if mode in ("keyboard", "mouse"):
            self.mode = mode
        else:
            print(f"Unsupported mode: {mode}")

    def handle_event(self, event):
        """Main event handler, calls different sub-handlers depending on mode."""
        if self.mode == "keyboard":
            self._handle_keyboard_event(event)
        else:
            self._handle_mouse_event(event)

    def _handle_keyboard_event(self, event):
        """Keyboard-based angle & power adjustment."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.angle = min(self.angle + 1, self.angle_max)
            elif event.key == pygame.K_DOWN:
                self.angle = max(self.angle - 1, self.angle_min)
            elif event.key == pygame.K_SPACE:
                self.charging = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.charging = False

    def _handle_mouse_event(self, event):
        """Mouse-drag for angle & power."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                self.mouse_drag = True
                self.drag_start_pos = pygame.mouse.get_pos()
                self.drag_current_pos = self.drag_start_pos
        elif event.type == pygame.MOUSEMOTION:
            if self.mouse_drag:
                self.drag_current_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_drag = False
                self._update_angle_power_from_drag(finalize=True)

    def update(self, dt):
        """Continuous update (e.g. for keyboard charging)."""
        # Keyboard charging
        if self.mode == "keyboard" and self.charging:
            self.power += dt * 30
            if self.power > self.max_power:
                self.power = self.max_power

        # Mouse drag (optional: do real-time angle/power)
        if self.mode == "mouse" and self.mouse_drag:
            self._update_angle_power_from_drag(finalize=False)

    def _update_angle_power_from_drag(self, finalize=False):
        """Computes angle & power from current drag positions."""
        if not self.drag_start_pos or not self.drag_current_pos:
            return
        sx, sy = self.drag_start_pos
        cx, cy = self.drag_current_pos
        dx, dy = (cx - sx), (sy - cy)  # invert y

        # Angle
        raw_angle = math.degrees(math.atan2(dy, dx))
        # Clamp
        self.angle = max(self.angle_min, min(self.angle_max, raw_angle))

        # Distance -> power
        dist = math.hypot(dx, dy)
        factor = 0.5  # scale factor
        self.power = min(dist * factor, self.max_power)

        if finalize:
            # user released mouse
            self.drag_start_pos = None
            self.drag_current_pos = None

    def get_throw_params(self):
        """Retrieves the current angle & power, typically called when finalizing throw."""
        return self.angle, self.power

    def reset(self):
        """Reset the angle/power if needed (after a throw)."""
        self.power = 0
        self.charging = False
        self.mouse_drag = False
        self.drag_start_pos = None
        self.drag_current_pos = None
