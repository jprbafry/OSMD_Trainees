import pygame
import math
import time
import random
import threading
from collections import deque
from dash_pygame.GUI import widget


# Plotter Class
class Plotter(widget.Widget):
    def __init__(self, x, y, width, height, min_val, max_val, color, font, auto=False):
        super().__init__(x, y, width, height, min_val, max_val)
        self.color = color
        self.font = font
        self.cur_val = (self.max_val-self.min_val)/2
        self.bg = widget.color_background
        self.data_buffer = deque(maxlen=width)
        self.auto = auto
        self.lock = threading.Lock()
        if self.auto:
            threading.Thread(target=self._generate_data, daemon=True).start()

    def update_cur_val(self, val):
        self.cur_val = val
        self.data_buffer.append(self.cur_val)

    def draw(self, surface):
        if not self.visible:
            return
        pygame.draw.rect(surface, self.bg, (self.x, self.y, self.width, self.height))
        with self.lock:
            ydata = list(self.data_buffer)
        if len(ydata) > 1:
            scale_y = self.height // 2 - 10
            prev_x = self.x
            prev_y = self.y + self.height // 2 - int(ydata[0] * scale_y)
            for i, val in enumerate(ydata):
                x = self.x + i
                y = self.y + self.height // 2 - int(val * scale_y)
                pygame.draw.line(surface, self.color, (prev_x, prev_y), (x, y))
                prev_x, prev_y = x, y

    def _generate_data(self):
        t = 0
        phase = random.uniform(0, math.pi)
        freq = random.uniform(1,5)
        amp = 0.8
        noise = (1-amp)*random.uniform(0, 1)
        while self.auto:
            with self.lock:
                self.cur_val = self.max_val*amp*math.sin(freq*t+phase) + self.max_val*noise
                self.data_buffer.append(self.cur_val)
            t += 0.05
            time.sleep(0.01)

        
if __name__ == "__main__":
    from dash_pygame.GUI import demo

    def plotter_factory(font):
        cx = 0
        cy = 100
        width = 300
        height = 100
        min_val = -1
        max_val = 1
        color = (255,255,0)
        return [Plotter(cx, cy, width, height, min_val, max_val, color, font, auto=True)]

    demo.run_widget_demo(plotter_factory)
