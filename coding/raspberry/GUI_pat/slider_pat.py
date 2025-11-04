import pygame


# SLIDER
class Slider:
    def __init__(self, x, y, width, font, min_val=0, max_val=180):
        self.x, self.y = x, y
        self.width = width
        self.min_val = min_val
        self.max_val = max_val
        self.old_des_val = max_val/2
        self.new_des_val = max_val/2
        self.old_cur_val = max_val/2
        self.new_cur_val = max_val/2
        self.dragging = False
        self.font = font

    def draw(self, surface):
        # Draw slider line
        pygame.draw.line(surface, color_line, (self.x, self.y), (self.x + self.width, self.y), 5)
        
        # Desired (red) circle
        pos_des = self.x + (self.new_des_val - self.min_val) / (self.max_val - self.min_val) * self.width
        pygame.draw.circle(surface, color_desired, (int(pos_des), self.y), 10, 5)

        # Current (green) circle
        pos_cur = self.x + (self.new_cur_val - self.min_val) / (self.max_val - self.min_val) * self.width
        pygame.draw.circle(surface, color_current, (int(pos_cur), self.y), 7, 3)

        # Draw desired value
        cur_des_txt = f"{int(self.new_cur_val)} ---> [{int(self.new_des_val)}]"
        val_text = self.font.render(cur_des_txt, True, color_text)
        text_rect = val_text.get_rect(center=(self.x + self.width / 2, self.y + self.width / 6))
        surface.blit(val_text, text_rect)

    def update_current_value(self, new_value):
        self.old_cur_val = self.new_cur_val
        self.new_cur_val = new_value

    def update_desired_value(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            pos = self.x + (self.new_des_val - self.min_val) / (self.max_val - self.min_val) * self.width
            if abs(mx - pos) < 10 and abs(my - self.y) < 15:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, _ = pygame.mouse.get_pos()
            mx = max(self.x, min(self.x + self.width, mx))
            self.old_des_val = self.new_des_val
            self.new_des_val = self.min_val + (mx - self.x) / self.width * (self.max_val - self.min_val)