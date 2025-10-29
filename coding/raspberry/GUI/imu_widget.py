import pygame
import math
import time
from IMU import IMU

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("IMU Accel + Gyro Visualization")
font = pygame.font.SysFont("consolas", 20)

imu = IMU(50, 150, 700, 300, font, screen)
clock = pygame.time.Clock()
t0 = time.time()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    t = time.time() - t0

    # Simulated accelerometer (g)
    ax = 0.5 * math.sin(t * 2)
    ay = 0.5 * math.sin(t * 1.5)
    az = 0.5 * math.sin(t * 1.2 + math.pi / 4)

    # Simulated gyroscope (°/s)
    gx = 50 * math.sin(t * 3)
    gy = 35 * math.sin(t * 2.3 + math.pi / 3)
    gz = 40 * math.sin(t * 1.7 + math.pi / 2)

    imu.set_values(ax, ay, az, gx, gy, gz)

    screen.fill((0, 0, 0))
    imu.draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
