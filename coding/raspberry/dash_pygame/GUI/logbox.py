import pygame
from dash_pygame.GUI import widget

class LogBox(widget.Widget):
    def __init__(self, x, y, width, height, font, max_logs=100):
        super().__init__(x=x, y=y, width=width, height=height)
        self.font = font
        self.max_logs = max_logs
        self.logs = []
        self.scroll_index = 0  # 0 = bottom (most recent log)
        self.line_height = self.font.get_linesize()
        self.scrollbar_width = 20
        self.button_height = 20
        self.mouse_hover = False

    def update_cur_val(self, text):
        if len(self.logs) >= self.max_logs:
            self.logs.pop(0)
        self.logs.append(text)
        self.scroll_index = 0  # auto-scroll to latest

    def draw(self, surface):
        if not self.visible:
            return

        # Draw main rectangle
        pygame.draw.rect(surface, (50, 50, 50), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, (200, 200, 200), (self.x, self.y, self.width, self.height), 2)

        # Calculate visible area for text
        text_width = self.width - self.scrollbar_width - 4
        text_height = self.height - 2

        # Draw logs
        max_lines = text_height // self.line_height
        start_index = max(0, len(self.logs) - self.scroll_index - max_lines)
        end_index = len(self.logs) - self.scroll_index
        visible_logs = self.logs[start_index:end_index]

        # Draw wrapped text
        y_offset = self.y + 2
        for line in visible_logs:
            wrapped_lines = self._wrap_text(line, text_width)
            for wline in wrapped_lines:
                text_surface = self.font.render(wline, True, (255, 255, 255))
                surface.blit(text_surface, (self.x + 2, y_offset))
                y_offset += self.line_height

        # Draw scroll bar background
        scrollbar_x = self.x + self.width - self.scrollbar_width
        pygame.draw.rect(surface, (80, 80, 80), (scrollbar_x, self.y, self.scrollbar_width, self.height))

        # Draw scroll buttons
        pygame.draw.rect(surface, (120, 120, 120), (scrollbar_x, self.y, self.scrollbar_width, self.button_height))  # Up button
        pygame.draw.polygon(surface, (255, 255, 255),
                            [(scrollbar_x + self.scrollbar_width//2, self.y + 5),
                             (scrollbar_x + 5, self.y + self.button_height - 5),
                             (scrollbar_x + self.scrollbar_width - 5, self.y + self.button_height - 5)])

        pygame.draw.rect(surface, (120, 120, 120), 
                         (scrollbar_x, self.y + self.height - self.button_height, self.scrollbar_width, self.button_height))  # Down button
        pygame.draw.polygon(surface, (255, 255, 255),
                            [(scrollbar_x + 5, self.y + self.height - self.button_height + 5),
                             (scrollbar_x + self.scrollbar_width - 5, self.y + self.height - self.button_height + 5),
                             (scrollbar_x + self.scrollbar_width//2, self.y + self.height - 5)])

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._mouse_over_scroll_up(event.pos):
                self.scroll_up()
            elif self._mouse_over_scroll_down(event.pos):
                self.scroll_down()
        elif event.type == pygame.MOUSEWHEEL:
            if self.mouse_hover:
                if event.y > 0:
                    self.scroll_up()
                else:
                    self.scroll_down()
        elif event.type == pygame.MOUSEMOTION:
            self.mouse_hover = self._mouse_over_box(event.pos)

    def scroll_up(self):
        if self.scroll_index < len(self.logs) - 1:
            self.scroll_index += 1

    def scroll_down(self):
        if self.scroll_index > 0:
            self.scroll_index -= 1

    def _wrap_text(self, text, max_width):
        """Wrap text to fit inside width"""
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    def _mouse_over_box(self, pos):
        x, y = pos
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def _mouse_over_scroll_up(self, pos):
        x, y = pos
        return self.x + self.width - self.scrollbar_width <= x <= self.x + self.width and \
               self.y <= y <= self.y + self.button_height

    def _mouse_over_scroll_down(self, pos):
        x, y = pos
        return self.x + self.width - self.scrollbar_width <= x <= self.x + self.width and \
               self.y + self.height - self.button_height <= y <= self.y + self.height


# Demo usage
if __name__ == "__main__":
    from dash_pygame.GUI import demo

    def logbox_factory(font):
        lb = LogBox(50, 50, 200, 200, font, max_logs=50)
        # Add some demo logs
        for i in range(100):
            lb.add_log(f"Log message {i}")
        return [lb]

    demo.run_widget_demo(logbox_factory)
