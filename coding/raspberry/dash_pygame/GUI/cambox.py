import pygame
import threading
import numpy as np
from camera.fake_picamera2 import Picamera2
from dash_pygame.GUI import widget  # base Widget class

class CamBox(widget.Widget):
    """
    CamBox widget: displays a frame (np.array) inside the widget.
    The frame can be updated externally via update_cur_val(frame).
    """
    def __init__(self, x, y, width, height, auto=False):
        super().__init__(x, y, width, height)
        # Initialize current frame with black image
        if self.width/1456 > self.height/1088:
            self.width = self.width
            self.height = int(self.width*1088/1456)
        else:
            self.width = int(self.height*1456/1088)
            self.height = self.height
        self.cur_val = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.auto = auto
        self.lock = threading.Lock()
        if self.auto:
            threading.Thread(target=self._generate_data, daemon=True).start()

    def update_cur_val(self, frame: np.ndarray):
        self.cur_val = frame.copy()

    def draw(self, surface: pygame.Surface):
        
        if not self.visible:
            return

        frame = self.cur_val.copy()

        # Convert BGR -> RGB for pygame
        frame_rgb = frame[..., ::-1]  # assumes input is BGR
        h, w = frame_rgb.shape[:2]

        # Convert to pygame surface
        frame_surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))

        # Compute scale factor to keep aspect ratio
        scale = min(self.width / w, self.height / h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        frame_scaled = pygame.transform.smoothscale(frame_surface, (new_w, new_h))

        # Compute offsets to center
        x_offset = (self.width - new_w) // 2
        y_offset = (self.height - new_h) // 2

        # Blit onto target surface
        target_surface = pygame.Surface((self.width, self.height))
        target_surface.fill((0, 0, 0))
        target_surface.blit(frame_scaled, (x_offset, y_offset))
        surface.blit(target_surface, (self.x, self.y))

    def _generate_data(self):
        picam2 = Picamera2()
        picam2.start()
        while self.auto:
            frame = picam2.capture_array()
            self.cur_val = frame.copy()


if __name__ == "__main__":
    from dash_pygame.GUI import demo

    def cambox_factory(font):
        
        cambox = CamBox(x=50, y=50, width=200, height=200, auto=True)

        return [cambox]  # always return a list of widgets

    demo.run_widget_demo(cambox_factory)