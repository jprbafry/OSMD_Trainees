import pygame
import threading
from dash_pygame.GUI import widget


class Indicator(widget.Widget):
    def __init__(self, x, y, size, auto=False):
        super().__init__(x, y, width=size, height=size)
        self.auto = auto
        self.lock = threading.Lock()
        self.color = (255, 0, 0,) #color red
    
    def update(self): #For structural purpose
        pass 

    def draw(self, surface): #Draws a single red circle
        if not self.visible:
            return
        
        with self.lock:
            color = self.color

        center = (self.x + self.width //2, self.y + self.height // 2)
        radius = self.width //  2 - 4
        pygame.draw.circle(surface, color, center, radius)

    def _generate_data(self):
        pass

#Main
if __name__ == "__main__":
    from dash_pygame.GUI import demo

    def indicator_factory(font):
        ind = Indicator(150, 100, 60, font)
        return [ind]
    
    demo.run_widget_demo(indicator_factory)

        
