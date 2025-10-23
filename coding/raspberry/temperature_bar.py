import Bar
import pygame
import threading
import time
import os

pygame.init()
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bars Demo")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

temperature_bar = Bar.Bar(x=100, y=100, width=50, height=255, min_val=0, max_val=60, colors=[(0,0,255),(255,255,255),(255,0,0)], label="Temperature", font=font, surface=screen)

running = True
while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw bars
    temperature_bar.set_value(25)  # Example to set value; in practice, this would be updated by the thread
    temperature_bar.draw()


    pygame.display.flip()
    clock.tick(30)

pygame.quit()