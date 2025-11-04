import pygame
import math
import threading
import random
import time
from GUI import widget

#Knob class
class Knob(widget.Widget):
    def __init__(self, cx, cy, radius, font, min_val=0, max_val=360, auto=False):
        self.cx, self.cy = cx, cy #position and size
        self.radius = radius
        self.min_val = min_val #valuye range
        self.max_val = max_val #value range
        self.angle = math.radians(min_val)
        self.old_cur_val = max_val/2
        self.new_cur_val = max_val/2
        self.dragging = False
        self.font = font
        if self.auto: #If auto mode, start data generation thread
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
        pygame.draw.line(surface, (255, 0, 0), (self.cx, self.cy), (end_x, end_y), 5)

        # # Draw value text
        # value_surf = self.font.render(f"{int(self.new_cur_val)}", True, (255, 255, 255))
        # surface.blit(value_surf, (self.cx - value_surf.get_width() // 2, self.cy + self.radius + 10))

    def _generate_data(self):
        t = 0
        freq = random.uniform(1,3) #random frequency
        amp = random.uniform(0.1,0.9) #random amplitude
        while self.auto:
            with self.lock:
                self.cur_val = self.max_val*amp + (1-amp)*self.max_val*math.sin(freq*t) #generate sine wave data
            t += 0.02
            time.sleep(0.01)


if __name__ == "__main__":
    from GUI import demo

    def knob_factory(font):
        radius = 60 #size of the knob (in pixels)
        cx = 150 #x position
        cy = 150 #y position
        min_val = 0 #minimum value
        max_val = 360 #maximum value
        knob = Knob(cx, cy, radius, font, min_val, max_val, auto=True) #setting auto True means that the knob will generate its own data 
        return knob

    demo.demo_widget(knob_factory)



    
