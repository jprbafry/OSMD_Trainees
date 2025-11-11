import pygame
import math
import time
import math
import threading
from dash_pygame.GUI import widget

# Slider Class
class Slider(widget.Widget):
    def __init__(self, x, y, width, height, min_val, max_val, font, auto=False):
        super().__init__(x, y, width, height, min_val, max_val)
        self.cur_val = (self.max_val-self.min_val)/2
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
        pygame.draw.line(surface, widget.color_line, (self.x, self.y), (self.x + self.width, self.y), 5)
        pos_cur = self.x + (self.cur_val - self.min_val) / (self.max_val - self.min_val) * self.width
        pygame.draw.circle(surface, widget.color_current, (int(pos_cur), self.y), 7, 3)

    def _generate_data(self):
        t = 0
        while self.auto:
            with self.lock:
                self.cur_val = self.max_val*0.5 + 0.2*self.max_val*math.sin(t)
            t += 0.002
            time.sleep(0.01)

if __name__ == "__main__":
    from dash_pygame.GUI import demo

    def slider_factory(font):
        cx = 50
        cy = 150
        width = 200
        height = 0
        min_val = 0
        max_val = 180
        slider = Slider(cx, cy, width, height, min_val, max_val, font, auto=True)
        return [slider] #always return a list of widgets

    demo.run_widget_demo(slider_factory)