import pygame
import math
from dash_pygame.GUI import widget


#LABEL CLASS 

class Label(widget.Widget):
    def __init__(self, text, x, y, font, color=widget.color_text, center=True, auto=True):
        super().__init__(x, y)
        self.text = text
        self.font = font
        self.auto = auto
        self.color = color
        self.center = center

    def update_cur_val(self, event=None):
        pass

    def draw(self, surface):
        if not self.visible:
            return
        text_surface = self.font.render(self.text, True, self.color)
        if self.center:
            text_rect = text_surface.get_rect(center=(self.x, self.y))
        else:
            text_rect = text_surface.get_rect(topleft=(self.x, self.y))
        surface.blit(text_surface, text_rect)

    def _generate_data(self):
        pass

    
#Main 
if __name__ == "__main__":
    from dash_pygame.GUI import demo


    def label_factory(font):
        label = Label("Hello Widget!", 150, 50, font, auto=True)
        return [label]

    demo.run_widget_demo(label_factory)