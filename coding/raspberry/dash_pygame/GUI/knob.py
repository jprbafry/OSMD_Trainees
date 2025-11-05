import pygame
import math
import threading
import random
import time


#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
from dash_pygame.GUI import widget

#Knob class
class Knob(widget.Widget):
    def __init__(self, cx, cy, radius, font, min_val=0, max_val=360, auto=False):
        # Call base Widget initializer
        super().__init__(x=cx, y=cy, width=radius*2, height=radius*2,
                         min_val=min_val, max_val=max_val)
        self.cx, self.cy = cx, cy
        self.radius = radius
        self.angle = math.radians(min_val)
        self.old_cur_val = max_val / 2
        self.new_cur_val = max_val / 2
        self.dragging = False
        self.font = font
        self.auto = auto
        if self.auto:
            self.lock = threading.Lock()
            threading.Thread(target=self._generate_data, daemon=True).start()

    def update_cur_val(self,val):
        self.new_cur_val = max(self.min_val, min(self.max_val, val))

    def draw(self, surface):
        if not self.visible:
            return
        # # Draw knob circle
        pygame.draw.circle(surface, (200, 200, 200), (self.cx, self.cy), self.radius)
        pygame.draw.circle(surface, (100, 100, 100), (self.cx, self.cy), self.radius, 5)

        # Draw knob indicator
        angle = math.radians(self.new_cur_val)
        end_x = self.cx + self.radius * 0.8 * math.cos(angle - math.pi / 2)
        end_y = self.cy + self.radius * 0.8 * math.sin(angle - math.pi / 2)
        pygame.draw.line(surface, (0, 0, 0), (self.cx, self.cy), (end_x, end_y), 5)

        # Draw home indicator
        home_angle = -math.pi / 2  # top
        home_x = self.cx + self.radius * 0.9 * math.cos(home_angle)
        home_y = self.cy + self.radius * 0.9 * math.sin(home_angle)
        pygame.draw.circle(surface, (255, 0, 0), (int(home_x), int(home_y)), 6)

        # # Draw value text
        # value_surf = self.font.render(f"{int(self.new_cur_val)}", True, (255, 255, 255))
        # surface.blit(value_surf, (self.cx - value_surf.get_width() // 2, self.cy + self.radius + 10))

    def _generate_data(self):
        t = 0
        freq = random.uniform(0.5, 2)
        while self.auto:
            with self.lock:
                self.new_cur_val = self.min_val + (self.max_val - self.min_val) * (0.5 + 0.5 * math.sin(freq * t))
            t += 0.05
            time.sleep(0.02)



if __name__ == "__main__":
    from dash_pygame.GUI import demo

    def knob_factory(font):
        radius = 60
        cx = 150
        cy = 150
        min_val = 0
        max_val = 360
        knob = Knob(cx, cy, radius, font, min_val, max_val, auto=True)
        return [knob]   # always return a list of widgets


    demo.run_widget_demo(knob_factory)



    
