import pygame
from GUI import knob
from GUI import plotter
from GUI import bar
from GUI import slider
from GUI import widget

class Panel:
    def __init__(self, auto=False):
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 600))
        pygame.display.set_caption("Widget System Demo + Bar")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.auto = auto

        # Widgets setup

        # Knobs
        self.knobs = [
            knob.Knob(150, 110, 60, 0, 360, self.font, auto=self.auto),
            knob.Knob(400, 110, 60, 0, 360, self.font, auto=self.auto)
        ]

        # Sliders
        self.sliders = [
            slider.Slider( 90, 210, 120, 0, 0, 180, self.font, auto=self.auto),
            slider.Slider(340, 210, 120, 0, 0, 180, self.font, auto=self.auto)
        ]

        # Plotters
        self.plotters = [
            plotter.Plotter( 50, 260, 200, 90, 1, -1, (255,0,0), self.font, auto=self.auto),
            plotter.Plotter( 50, 360, 200, 90, 1, -1, (0,255,0), self.font, auto=self.auto),
            plotter.Plotter( 50, 460, 200, 90, 1, -1, (0,0,255), self.font, auto=self.auto),
            plotter.Plotter(300, 260, 200, 90, 1, -1, (255,255,0), self.font, auto=self.auto),
            plotter.Plotter(300, 360, 200, 90, 1, -1, (0,255,255), self.font, auto=self.auto),
            plotter.Plotter(300, 460, 200, 90, 1, -1, (255,0,255), self.font, auto=self.auto)
        ]

        # Bars
        c_b1 = [(0, 0, 255), (255,255,255), (255, 0, 0)]
        c_b2 = [(255,255,255), (255, 165, 0)]
        self.bars = [
            bar.Bar(550, 50, 30, 500, 0, 100, c_b1, "B 1", self.font, auto=self.auto),
            bar.Bar(600, 50, 30, 500, 0, 1024, c_b2, "B 2", self.font, auto=self.auto)
        ]

        # All widgets together for easy drawing
        self.widgets = self.knobs + self.sliders + self.plotters + self.bars

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