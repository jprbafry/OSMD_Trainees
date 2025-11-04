import pygame
import threading
import time
import os


# ------------------------
# Bar class
# ------------------------
class Bar:
    def __init__(self, x, y, width, height, min_val, max_val, colors, label, font, surface):
        """
        x, y: top-left corner
        width, height: dimensions of the bar
        min_val, max_val: values corresponding to bottom/top
        colors: list of 2 or 3 colors [(bottom), (middle), (top)]
        label: text label
        font: pygame font object
        surface: pygame surface to draw on
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.colors = colors
        self.label = label
        self.font = font
        self.surface = surface
        self.current_val = min_val  # initial value
        self.rect_height = 5  # height of marker rectangle

    def set_value(self, val):
        # Clamp value
        self.current_val = max(self.min_val, min(self.max_val, val))

    def draw(self):
        # Draw label
        label_surf = self.font.render(self.label, True, (255, 255, 255))
        self.surface.blit(label_surf, (self.x, self.y - 25))

        # Draw gradient bar
        for i in range(self.height):
            ratio = i / self.height
            color = self.get_color(ratio)
            pygame.draw.line(self.surface, color, 
                             (self.x, self.y + self.height - i),
                             (self.x + self.width, self.y + self.height - i))

        # Draw marker rectangle
        value_ratio = (self.current_val - self.min_val) / (self.max_val - self.min_val)
        marker_y = self.y + self.height - int(value_ratio * self.height)
        pygame.draw.rect(self.surface, (255, 255, 255),
                         (self.x, marker_y - self.rect_height//2, self.width, self.rect_height))

    def get_color(self, ratio):
        """Compute the color at given ratio (0 bottom -> 1 top)"""
        if len(self.colors) == 2:
            bottom, top = self.colors
            return tuple(int(bottom[i] + (top[i] - bottom[i]) * ratio) for i in range(3))
        elif len(self.colors) == 3:
            bottom, middle, top = self.colors
            if ratio < 0.5:
                # bottom -> middle
                local_ratio = ratio / 0.5
                return tuple(int(bottom[i] + (middle[i] - bottom[i]) * local_ratio) for i in range(3))
            else:
                # middle -> top
                local_ratio = (ratio - 0.5) / 0.5
                return tuple(int(middle[i] + (top[i] - middle[i]) * local_ratio) for i in range(3))
        else:
            return (255, 255, 255)  # fallback

# ------------------------
# Thread to update values
# ------------------------
def value_updater(file_path, temp_bar):
    while True:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    try:
                        temp_val = float(lines[0].strip())
                        temp_bar.set_value(temp_val)
                    except ValueError:
                        pass  # ignore malformed lines
        time.sleep(0.1)  # update rate

#To test the bar
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Test Bar")
    font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()

    # Create a bar instance
    bar = Bar(
        x=100, y=30, width=50, height=200,
        min_val=0, max_val=60,
        colors=[(0, 0, 255), (255, 255, 255), (255, 0, 0)],
        label="Bar Test",
        font=font,
        surface=screen
    )

    # Set initial test value
    bar.set_value(30)  # 30°C for testing

    running = True
    while running:
        screen.fill((0, 0, 0))  # black background
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        bar.draw()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
