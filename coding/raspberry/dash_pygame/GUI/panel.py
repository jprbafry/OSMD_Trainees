import pygame

from dash_pygame.GUI import widget
from dash_pygame.GUI import plotter
from dash_pygame.GUI import bar
from dash_pygame.GUI import knob
from dash_pygame.GUI import slider
from dash_pygame.GUI import label
from dash_pygame.GUI import logbox
from dash_pygame.GUI import indicator


class Panel:
    def __init__(self, auto=False):
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 600))
        pygame.display.set_caption("Widget System Demo + Bar")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.auto = auto

        # Knobs
        self.knobs = [
            knob.Knob(150, 110, 60, self.font, 0, 360, auto=self.auto),
            knob.Knob(400, 110, 60, self.font, 0, 360, auto=self.auto),
        ]
        # Knobs Home Indicator
        self.knobs_indicators = [
            indicator.Indicator(self.knobs[0].cx - self.knobs[0].radius // 7, self.knobs[0].cy - self.knobs[0].radius -5, 16),
            indicator.Indicator(self.knobs[1].cx - self.knobs[0].radius // 7, self.knobs[0].cy - self.knobs[0].radius -5, 16),
        ]

        # Sliders
        self.sliders = [
            slider.Slider(50, 200, 200, 0, 0, 180, self.font, auto=self.auto),
            slider.Slider(300, 200, 200, 0, 0, 180, self.font, auto=self.auto),
        ]

        # Sliders Home Indicator
        self.sliders_indicators = [
            indicator.Indicator(self.sliders[0].x -6,self.sliders[0].y -7 ,14), #left slider
            indicator.Indicator(self.sliders[1].x -6, self.sliders[1].y -7,14), #right slider
        ]


        # Plotters
        self.plotters = [
        plotter.Plotter(50, 250, 200, 100, 1, -1, (255,0,0), self.font, auto=self.auto),
        plotter.Plotter(50, 350, 200, 100, 1, -1, (0,255,0), self.font, auto=self.auto),
        plotter.Plotter(50, 450, 200, 100, 1, -1, (0,0,255), self.font, auto=self.auto),
        plotter.Plotter(300, 250, 200, 100, 1, -1, (255,255,0), self.font, auto=self.auto),
        plotter.Plotter(300, 350, 200, 100, 1, -1, (0,255,255), self.font, auto=self.auto),
        plotter.Plotter(300, 450, 200, 100, 1, -1, (255,0,255), self.font, auto=self.auto),
        ]

        # Bars
        c_b1 = [(0, 0, 255), (255,255,255), (255, 0, 0)]
        c_b2 = [(255,255,255), (255, 165, 0)]
        self.bars = [
        bar.Bar(550, 50, 30, 500, 0, 100, c_b1, "B 1", self.font, auto=self.auto),
        bar.Bar(600, 50, 30, 500, 0, 1024, c_b2, "B 2", self.font, auto=self.auto),
        ]


        # All widgets together for easy drawing
        self.widgets = self.knobs + self.sliders + self.plotters + self.bars + self.knobs_indicators + self.sliders_indicators

    def draw(self):
        """Draw all widgets"""
        self.screen.fill(widget.color_background)
        for w in self.widgets:
            w.draw(self.screen)
        pygame.display.flip()

    def tick(self, fps=60):
        """Control frame rate"""
        self.clock.tick(fps)


if __name__ == "__main__":

    panel = Panel(auto=True)
    running = True
    while running:
        panel.draw()
        panel.tick()