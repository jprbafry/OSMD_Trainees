import pygame
import math
from collections import deque

class IMUPlot:
    def __init__(self, x, y, width, height, font, surface, max_points=800): #setting up the Plot
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.surface = surface
        self.max_points = max_points #new points push out the oldest points

        # Data buffers. When a new value is added, the oldest is removed automatially
        self.data_ax = deque([0]*max_points, maxlen=max_points)
        self.data_ay = deque([0]*max_points, maxlen=max_points)
        self.data_az = deque([0]*max_points, maxlen=max_points)
        self.data_gx = deque([0]*max_points, maxlen=max_points)
        self.data_gy = deque([0]*max_points, maxlen=max_points)
        self.data_gz = deque([0]*max_points, maxlen=max_points)

        # Colors for plotting
        self.color_ax = (255, 200, 0)   # orange
        self.color_ay = (0, 255, 100)   # green
        self.color_az = (0, 150, 255)   # blue
        self.color_gx = (255, 80, 80)   # red
        self.color_gy = (255, 105, 180) # pink
        self.color_gz = (150, 80, 255)  # purple

        # Mid-lines, center baselines for accel and gyro plots
        self.mid_y_accel = self.y + self.height // 3
        self.mid_y_gyro = self.y + 2 * self.height // 3

    #Updates the data buffers with new IMU values
    def set_values(self, ax, ay, az, gx=None, gy=None, gz=None):
        self.data_ax.append(ax)
        self.data_ay.append(ay)
        self.data_az.append(az)
        if gx is not None and gy is not None and gz is not None: #checks whether gyro data is provided
            self.data_gx.append(gx)
            self.data_gy.append(gy)
            self.data_gz.append(gz)

    def draw(self):
        # Draw background
        pygame.draw.rect(self.surface, (10, 10, 30), (self.x, self.y, self.width, self.height))

        pygame.draw.line(self.surface, (60, 60, 80), (self.x, self.mid_y_accel), (self.x + self.width, self.mid_y_accel), 1)
        pygame.draw.line(self.surface, (60, 60, 80), (self.x, self.mid_y_gyro), (self.x + self.width, self.mid_y_gyro), 1)

        def map_y_accel(val): return int(self.mid_y_accel - val * 100)
        def map_y_gyro(val): return int(self.mid_y_gyro - val * 1)

        self._draw_wave(self.data_ax, self.color_ax, map_y_accel)
        self._draw_wave(self.data_ay, self.color_ay, map_y_accel)
        self._draw_wave(self.data_az, self.color_az, map_y_accel)

        self._draw_wave(self.data_gx, self.color_gx, map_y_gyro)
        self._draw_wave(self.data_gy, self.color_gy, map_y_gyro)
        self._draw_wave(self.data_gz, self.color_gz, map_y_gyro)

        label_acc = self.font.render("Accelerometer (g)", True, (255, 255, 255))
        label_gyro = self.font.render("Gyroscope (°/s)", True, (255, 255, 255))
        self.surface.blit(label_acc, (self.x, self.mid_y_accel - 25))
        self.surface.blit(label_gyro, (self.x, self.mid_y_gyro - 25))

    def _draw_wave(self, data, color, map_y):
        if len(data) < 2:
            return
        points = []
        for i, val in enumerate(data):
            px = self.x + i
            py = map_y(val)
            points.append((px, py))
        pygame.draw.lines(self.surface, color, False, points, 2)
