
import time
import tkinter as tk
from src.utils.executor import run_cmd

class MouseController:
    def __init__(self, sensitivity: float = 1.5):
        self.sensitivity = sensitivity
        self.screen_w, self.screen_h = self._get_screen_size()
        self.prev_x, self.prev_y = None, None
        self.last_click = 0
        self.click_cooldown = 0.3
        self.left_down = False

    def _get_screen_size(self):
        try:
            root = tk.Tk()
            root.withdraw()
            w, h = root.winfo_screenwidth(), root.winfo_screenheight()
            root.destroy()
            return w, h
        except:
            return 1920, 1080

    def move_relative(self, x_norm: float, y_norm: float):
        if self.prev_x is None:
            self.prev_x, self.prev_y = x_norm, y_norm
            return

        dx = (x_norm - self.prev_x) * self.screen_w * self.sensitivity
        dy = (y_norm - self.prev_y) * self.screen_h * self.sensitivity

        if abs(dx) > 1 or abs(dy) > 1:
            run_cmd(['ydotool', 'mousemove', '-x', str(int(dx)), '-y', str(int(dy))])

        self.prev_x, self.prev_y = x_norm, y_norm

    def reset(self):
        self.prev_x, self.prev_y = None, None
        self.toggle_drag(False)

    def click(self, right: bool = False):
        if time.time() - self.last_click > self.click_cooldown:
            code = '0x41' if right else '0x40'
            run_cmd(['ydotool', 'click', code])
            run_cmd(['ydotool', 'click', hex(int(code, 16) + 0x40)]) 
            self.last_click = time.time()
            return True
        return False

    def toggle_drag(self, active: bool):
        if active and not self.left_down:
            run_cmd(['ydotool', 'click', '0x40'])
            self.left_down = True
        elif not active and self.left_down:
            run_cmd(['ydotool', 'click', '0x80'])
            self.left_down = False

    def scroll(self, amount: int):
        if amount == 0: return
        run_cmd(['ydotool', 'mousemove', '-w', '--', '0', str(amount)])