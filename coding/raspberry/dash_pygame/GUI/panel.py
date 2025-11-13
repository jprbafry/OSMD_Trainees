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
        self.screen = pygame.display.set_mode((1500, 750))
        pygame.display.set_caption("Widget System Demo + Bar")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 21)
        self.font_small = pygame.font.SysFont(None, 15)
        self.auto = auto

        #Knobs
        self.knobs = [
            knob.Knob(150, 115, 50, self.font, 0, 360, auto=self.auto),
            knob.Knob(400, 115, 50, self.font, 0, 360, auto=self.auto),
        ]
        #Knobs Home Indicator
        self.knobs_indicators = [
            indicator.Indicator(self.knobs[0].cx - self.knobs[0].radius // 7, self.knobs[0].cy - self.knobs[0].radius -5, 16),
            indicator.Indicator(self.knobs[1].cx - self.knobs[1].radius // 7, self.knobs[1].cy - self.knobs[1].radius -5, 16),
        ]

        #Sliders
        self.sliders = [
            slider.Slider(70, 275, 150, 0, 0, 180, self.font, auto=self.auto),
            slider.Slider(330, 275, 150, 0, 0, 180, self.font, auto=self.auto),
        ]

        #Sliders Home Indicator
        self.sliders_indicators = [
            indicator.Indicator(self.sliders[0].x -6,self.sliders[0].y -7 ,14), #left slider
            indicator.Indicator(self.sliders[1].x -6, self.sliders[1].y -7,14), #right slider
        ]


        #Plotters
        self.plotters = [
        plotter.Plotter(50, 400, 200, 100, 1, -1, (255,0,0), self.font, auto=self.auto),
        plotter.Plotter(50, 500, 200, 100, 1, -1, (0,255,0), self.font, auto=self.auto),
        plotter.Plotter(50, 600, 200, 100, 1, -1, (0,0,255), self.font, auto=self.auto),
        plotter.Plotter(300, 400, 200, 100, 1, -1, (255,255,0), self.font, auto=self.auto),
        plotter.Plotter(300, 500, 200, 100, 1, -1, (0,255,255), self.font, auto=self.auto),
        plotter.Plotter(300, 600, 200, 100, 1, -1, (255,0,255), self.font, auto=self.auto),
        ]

        #Bars
        c_b1 = [(0, 0, 255), (255,255,255), (255, 0, 0)]
        c_b2 = [(255,255,255), (255, 165, 0)]
        self.bars = [
        bar.Bar(650, 80, 30, 600, 0, 100, c_b1, "", self.font, auto=self.auto),
        bar.Bar(750, 80, 30, 600, 0, 1024, c_b2, "", self.font, auto=self.auto),
        ]

        #Logbox
        self.logbox = logbox.LogBox(900, 500, 500, 200, self.font_small, max_lines=8, auto=self.auto)
        self.logbox.add_line("System initialized...")
        self.logbox.add_line("Dashboard started.")

        #General labels
        self.labels = []

        #Label for Bar 1(temp)
        b1 = self.bars[0]
        label_x = b1.x + b1.width // 2
        label_y = b1.y - 40
        lbl1 = label.Label("Temperature", label_x, label_y, self.font, center=True)
        self.labels.append(lbl1)

        #Label for Bart 2 (light intensity)
        b2 = self.bars[1]
        label_x = b2.x + b2.width // 2 + 15
        label_y = b2.y - 40
        lbl2 = label.Label("Light Intensity", label_x, label_y, self.font, center=True)
        self.labels.append(lbl2)

        #Label for Knob 1
        k1 = self.knobs[0]
        label_x = k1.cx 
        label_y = k1.cy -k1.radius - 40
        lbl1 = label.Label("Azimuthal", label_x, label_y, self.font, center=True)
        self.labels.append(lbl1)

        #Label for Knob 2
        k2 = self.knobs[1]
        label_x = k2.cx 
        label_y = k2.cy -k2.radius - 40
        lbl2 = label.Label("Azimuthal", label_x, label_y, self.font, center=True)
        self.labels.append(lbl2)

        #Label for slider 1
        s1 = self.sliders[0]
        label_x = s1.x + s1.width // 2
        label_y = s1.y - 40
        lbl_s1 = label.Label("Polar", label_x, label_y, self.font, center=True)
        self.labels.append(lbl_s1)

        #Label for slider 2
        s2 = self.sliders[1]
        label_x = s2.x + s2.width // 2
        label_y = s2.y - 40
        lbl_s2 = label.Label("Polar", label_x, label_y, self.font, center=True)
        self.labels.append(lbl_s2)

        #Label for accelerometer
        p_left = self.plotters[0]
        label_x = p_left.x + p_left.width // 2
        label_y = p_left.y - 40
        lbl_p_left = label.Label("Accelerometer", label_x, label_y, self.font, center=True)
        self.labels.append(lbl_p_left)

        #Label for gyro
        p_right = self.plotters[3]
        label_x = p_right.x + p_right.width // 2
        label_y = p_right.y - 40
        lbl_p_right = label.Label("Gyro", label_x, label_y, self.font, center=True)
        self.labels.append(lbl_p_right)

        #Label for LogBox
        label_x = self.logbox.x + self.logbox.width // 2
        label_y = self.logbox.y - 25
        lbl_log = label.Label("System Log", label_x, label_y, self.font, center=True)
        self.labels.append(lbl_log)

        # All widgets together for easy drawing
        self.widgets = self.knobs + self.sliders + self.plotters + self.bars + self.knobs_indicators + self.sliders_indicators + self.labels + [self.logbox]

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