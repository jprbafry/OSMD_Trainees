import pygame

from dash_pygame.GUI import widget
from dash_pygame.GUI import plotter
from dash_pygame.GUI import bar
from dash_pygame.GUI import knob
from dash_pygame.GUI import slider
from dash_pygame.GUI import cambox
from dash_pygame.GUI import logbox
from dash_pygame.GUI import label

class Panel:
    def __init__(self, auto=False):

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((1120, 600))
        pygame.display.set_caption("OSMD's PyGame Dashboard")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.auto = auto

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
            plotter.Plotter(50, 250, 200, 100, 1, -1, (255,0,0), self.font, auto=self.auto),
            plotter.Plotter(50, 350, 200, 100, 1, -1, (0,255,0), self.font, auto=self.auto),
            plotter.Plotter(50, 450, 200, 100, 1, -1, (0,0,255), self.font, auto=self.auto),
            plotter.Plotter(300, 250, 200, 100, 1, -1, (255,255,0), self.font, auto=self.auto),
            plotter.Plotter(300, 350, 200, 100, 1, -1, (0,255,255), self.font, auto=self.auto),
            plotter.Plotter(300, 450, 200, 100, 1, -1, (255,0,255), self.font, auto=self.auto)
        ]

        # Bars
        c_b1 = [(0, 0, 255), (255,255,255), (255, 0, 0)]
        c_b2 = [(255,255,255), (255, 165, 0)]
        self.bars = [
            bar.Bar(550, 50, 30, 500, 0, 100, c_b1, self.font, auto=self.auto),
            bar.Bar(600, 50, 30, 500, 0, 1024, c_b2, self.font, auto=self.auto)
        ]

        # CamBox
        self.cambox = [cambox.CamBox(x=670, y=50, width=300, height=300, auto=self.auto)]

        # LogBox
        self.logbox = [logbox.LogBox(670, 400, 400, 150, self.font, max_logs=100)]


        # All widgets together for easy drawing
        self.widgets = self.knobs + self.sliders + self.plotters + self.bars + self.cambox + self.logbox

    def draw(self):
        """Draw all widgets"""
        self.screen.fill(widget.color_background)
        for w in self.widgets:
            w.draw(self.screen)
        pygame.display.flip()

    def handle_events(self):        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # Pass event to widgets if they have handle_event
            for w in self.widgets:
                if hasattr(w, "handle_event"):
                    w.handle_event(event)

    def tick(self, fps=60):
        """Control frame rate"""
        self.clock.tick(fps)


if __name__ == "__main__":

    panel = Panel(auto=True)
    running = True
    while running:
        panel.draw()
        panel.tick()