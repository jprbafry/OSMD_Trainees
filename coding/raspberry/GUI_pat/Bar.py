import pygame
import threading
import math
import random
import time
from GUI_pat import widget

def get_color(ratio, colors):
    if len(colors) == 2:
        bottom, top = colors
        return tuple(int(bottom[i] + (top[i] - bottom[i]) * ratio) for i in range(3))
    elif len(colors) == 3:
        bottom, middle, top = colors
        if ratio < 0.5:
            local_ratio = ratio / 0.5
            return tuple(int(bottom[i] + (middle[i] - bottom[i]) * local_ratio) for i in range(3))
        else:
            local_ratio = (ratio - 0.5) / 0.5
            return tuple(int(middle[i] + (top[i] - middle[i]) * local_ratio) for i in range(3))
    else:
        return (255, 255, 255)

# Bar Class
class Bar(widget.Widget):
    def __init__(self, x, y, width, height, min_val, max_val, colors, label, font, auto=False):
        super().__init__(x, y, width, height, min_val, max_val)
        self.cur_val = (self.max_val-self.min_val)/2
        self.colors = colors
        self.label = label
        self.font = font
        self.rect_height = 5
        self.auto = auto
        if self.auto:
            self.lock = threading.Lock()
            threading.Thread(target=self._generate_data, daemon=True).start()

    def update_cur_val(self, val):
        self.cur_val = max(self.min_val, min(self.max_val, val))

    def draw(self, surface):
        if not self.visible:
            return
        # Label
        label_surf = self.font.render(self.label, True, (255, 255, 255))
        surface.blit(label_surf, (self.x, self.y - 25))
        # Gradient bar
        for i in range(self.height):
            ratio = i / self.height
            color = get_color(ratio, self.colors)
            pygame.draw.line(surface, color,
                             (self.x, self.y + self.height - i),
                             (self.x + self.width, self.y + self.height - i))
        # Marker
        value_ratio = (self.cur_val - self.min_val) / (self.max_val - self.min_val)
        marker_y = self.y + self.height - int(value_ratio * self.height)
        pygame.draw.rect(surface, (255, 255, 255),
                         (self.x, marker_y - self.rect_height // 2, self.width, self.rect_height))

    def _generate_data(self):
        t = 0
        phase = random.uniform(0, math.pi)
        freq = random.uniform(0.1,0.5)
        amp = random.uniform(0.5,0.9)
        while self.auto:
            with self.lock:
                self.cur_val = self.max_val*amp + (1-amp)*self.max_val*math.sin(freq*t+phase)
            t += 0.10
            time.sleep(0.01)

if __name__ == "__main__":
    from GUI import demo

    def bar_factory(font):
        
        width = 30
        cx = 150-width/2
        cy = 50
        height = 200
        min_val = 0
        max_val = 100
        colors = [(0, 0, 255), (255, 255, 0), (255, 0, 0)]
        text = "Bar"
        bar = Bar(cx, cy, width, height, min_val, max_val, colors, text, font, auto=True)

        return [bar]  # always return a list of widgets

    demo.run_widget_demo(bar_factory)