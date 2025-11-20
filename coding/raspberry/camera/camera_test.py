import pygame
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from camera.fake_camera import Picamera2
import cv2
import numpy as np

# Initialize pygame
window_size = 400      
screen = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("FakeCam Pygame")

# Initialize fake camera
picam2 = Picamera2()
picam2.start()

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the frame from the fake camera
    frame = picam2.capture_array()  # H x W x 3, BGR

    # Convert BGR -> RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert to pygame surface
    frame_surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))

    # --- Compute scale factor to keep aspect ratio ---
    frame_h, frame_w = frame.shape[:2]
    scale = min(window_size / frame_w, window_size / frame_h)
    new_w = int(frame_w * scale)
    new_h = int(frame_h * scale)

    # Scale the frame
    frame_scaled = pygame.transform.smoothscale(frame_surface, (new_w, new_h))

    # Compute offsets to center the image
    x_offset = (window_size - new_w) // 2
    y_offset = (window_size - new_h) // 2

    # Fill background with black
    screen.fill((0, 0, 0))

    # Blit the scaled image at centered position
    screen.blit(frame_scaled, (x_offset, y_offset))
    pygame.display.flip()

    # Limit FPS
    clock.tick(50)

picam2.stop()
pygame.quit()