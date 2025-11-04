import abc
import pygame


class Widget(abc.ABC):
    def __init__(self, x, y, width, height, label, font, surface):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.font = font
        self.surface = surface
        self.current_val = 0  # Common for visual widgets

    @abc.abstractmethod
    def set_value(self, value):
        """Update the widget's value."""
        pass

    @abc.abstractmethod
    def draw(self):
        """Draw the widget on the surface."""
        pass


# --------------------------------------------------------------------
# 👇 Temporary dummy subclass for testing the abstract Widget
# --------------------------------------------------------------------
class DummyWidget(Widget):
    def set_value(self, value):
        self.current_val = value

    def draw(self):
        # Draw a simple rectangle with the current value as text
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.surface, (0, 255, 0), rect)
        if self.font:
            text = self.font.render(f"{self.label}: {self.current_val}", True, (255, 255, 255))
            self.surface.blit(text, (self.x, self.y - 20))


# --------------------------------------------------------------------
# 👇 Run test when executed directly
# --------------------------------------------------------------------
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Widget Test")

    font = pygame.font.Font(None, 24)
    widget = DummyWidget(150, 100, 100, 80, "Demo", font, screen)

    running = True
    clock = pygame.time.Clock()
    val = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Simulate data updates
        val = (val + 1) % 100
        widget.set_value(val)

        # Draw everything
        screen.fill((0, 0, 0))
        widget.draw()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
