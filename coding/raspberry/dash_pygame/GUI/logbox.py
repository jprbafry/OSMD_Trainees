import pygame
import threading
from dash_pygame.GUI import widget


class LogBox(widget.Widget):
    """A simple scrolling text box for displaying logs in the dashboard."""
    def __init__(self, x, y, width, height, font, max_lines=10, auto=True):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.font = font
        self.auto = auto
        self.max_lines = max_lines
        self.lines = []
        self.lock = threading.Lock()
        self.bg_color = (20, 20, 20)
        self.text_color = (255, 255, 255)
        self.border_color = (255, 255, 255)

        # If auto=True, start demo thread to add random messages
        if self.auto:
            threading.Thread(target=self._auto_update, daemon=True).start()

    def add_line(self, text):
        """Add a new line to the log box."""
        with self.lock:
            self.lines.append(text)
            # Keep only the latest N lines
            if len(self.lines) > self.max_lines:
                self.lines = self.lines[-self.max_lines:]

    def draw(self, surface):
        if not self.visible:
            return

        # Draw background
        pygame.draw.rect(surface, self.bg_color, (self.x, self.y, self.width, self.height))
        # Draw border
        pygame.draw.rect(surface, self.border_color, (self.x, self.y, self.width, self.height), 2)

        # Draw text lines
        with self.lock:
            y_offset = self.y + 5
            for line in self.lines:
                text_surface = self.font.render(line, True, self.text_color)
                surface.blit(text_surface, (self.x + 5, y_offset))
                y_offset += text_surface.get_height() + 2

    def _auto_update(self):
        """Automatically add demo messages if auto mode is enabled."""
        import time, random
        demo_msgs = [
            "System initialized.",
            "Sensor A connected.",
            "Reading temperature...",
            "Data updated.",
            "Connection stable.",
            "Warning: High value detected.",
        ]
        while True:
            self.add_line(random.choice(demo_msgs))
            time.sleep(1.5)


# ----------------------------------------------------------
# Standalone test (for development)
# ----------------------------------------------------------
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("LogBox Demo")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 20)

    log = LogBox(50, 50, 300, 200, font, max_lines=8, auto=True)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(widget.color_background)
        log.draw(screen)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
