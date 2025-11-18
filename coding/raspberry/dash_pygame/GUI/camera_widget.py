import pygame
import numpy as np
import cv2
from dash_pygame.GUI import widget


class CameraWidget(widget.Widget):
    def __init__(self, x, y, width, height, camera, auto=True):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.camera = camera
        self.auto = auto
        self.bg_color = (0, 0, 0)

    def update_cur_val(self, event=None):
        pass  # No interaction

    def draw(self, surface):
        if not self.visible:
            return

        frame = self.camera.capture_array()  # BGR
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))
        scaled_frame = pygame.transform.smoothscale(frame_surface, (self.width, self.height))
        surface.blit(scaled_frame, (self.x, self.y))


#Test the camera widget
if __name__ == "__main__":
    from camera.fake_camera import Picamera2

    pygame.init()
    window_size = 400
    screen = pygame.display.set_mode((window_size, window_size))
    pygame.display.set_caption("FakeCam Pygame")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 20)
    picam2 = Picamera2()
    picam2.start()

    camera_widget = CameraWidget(0, 0, window_size, window_size, picam2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        camera_widget.draw(screen)
        pygame.display.flip()
        clock.tick(50)

    picam2.stop()
    pygame.quit()
