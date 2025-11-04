import pygame
import sys, os
from Temperature_widget import TemperatureWidget 

#Dashboard class to manage multiple widgets
class Dashboard:
    def __init__(self):
        self.fps = 30 #frames per second (refresh rate)
        WIDTH, HEIGHT = 400, 400

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sensor Dashboard")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

        # Create widget instance
        self.temp_widget = TemperatureWidget(x=100, y=50, font=self.font, surface=self.screen)

        # Manage widgets
        self.widgets = [self.temp_widget]

    def update_temperature(self, value):
        self.temp_widget.update(value)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0, 0, 0))  # black background

            for widget in self.widgets:
                widget.draw()

            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()
