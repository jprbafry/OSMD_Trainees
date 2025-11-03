import pygame
from itertools import chain
from collections import deque
from GUI import widget
from GUI.knob import Knob
from GUI.slider import Slider
from GUI.plotter import Plotter
from GUI.label import Label
from GUI.bar import Bar






if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption("Widget System Demo + Bar")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    c_b1 = [(0, 0, 255), (255,255,255), (255, 0, 0)]
    c_b2 = [(255,255,255), (255, 165, 0)]

    knob_1 = Knob(150, 110, 60, 0, 360, font, auto=True)
    knob_2 = Knob(400, 110, 60, 0, 360, font, auto=True)
    plotter_1 = Plotter(50, 250, 200, 100, 1, -1, (255,0,0), font, auto=True)
    plotter_2 = Plotter(50, 350, 200, 100, 1, -1, (0,255,0), font, auto=True)
    plotter_3 = Plotter(50, 450, 200, 100, 1, -1, (0,0,255), font, auto=True)
    plotter_4 = Plotter(300, 250, 200, 100, 1, -1, (255,255,0), font, auto=True)
    plotter_5 = Plotter(300, 350, 200, 100, 1, -1, (0,255,255), font, auto=True)
    plotter_6 = Plotter(300, 450, 200, 100, 1, -1, (255,0,255), font, auto=True)
    bar_1 = Bar(550, 50, 30, 500, 0, 100, c_b1, "B 1", font, auto=True)
    bar_2 = Bar(600, 50, 30, 500, 0, 100, c_b2, "B 2", font, auto=True)

    widgets = [knob_1, knob_2, plotter_1, plotter_2, plotter_3, plotter_4, plotter_5, plotter_6, bar_1, bar_2]

    running = True
    while running:
        screen.fill(widget.color_background)
        for w in widgets:
            w.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
