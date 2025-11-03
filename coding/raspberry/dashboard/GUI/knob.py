import pygame
import threading
import math
import time
import random
from GUI import widget


# Knob Class
class Knob(widget.Widget):
    def __init__(self, cx, cy, radius, min_val, max_val, font, auto=False):
        super().__init__(cx, cy, radius*2, radius*2, min_val, max_val)
        self.cx, self.cy = cx, cy
        self.radius = radius
        self.angle = math.radians(min_val)
        self.cur_val = max_val/2
        self.dragging = False
        self.font = font
        self.auto = auto
        if self.auto:
            self.lock = threading.Lock()
            threading.Thread(target=self._generate_data, daemon=True).start()

    def update_cur_val(self, val):
        self.cur_val = val

    def draw(self, surface):
        if not self.visible:
            return
        pygame.draw.circle(surface, widget.color_line, (self.cx, self.cy), self.radius, 5)
        px_cur = self.cx + self.radius * math.cos(math.radians(self.cur_val) - math.pi / 2)
        py_cur = self.cy + self.radius * math.sin(math.radians(self.cur_val) - math.pi / 2)
        pygame.draw.line(surface, widget.color_current, (self.cx, self.cy), (px_cur, py_cur), 3)

    def _generate_data(self):
        t = 0
        freq = random.uniform(1,3)
        amp = random.uniform(0.1,0.9)
        while self.auto:
            with self.lock:
                self.cur_val = self.max_val*amp + (1-amp)*self.max_val*math.sin(freq*t)
            t += 0.01
            time.sleep(0.01)

if __name__ == "__main__":
    from GUI import demo

    def knob_factory(font):
        cx = 150
        cy = 150
        radius = 60
        min_val = 0
        max_val = 360
        return [Knob(cx, cy, radius, min_val, max_val, font, auto=True)]

    demo.run_widget_demo(knob_factory)
