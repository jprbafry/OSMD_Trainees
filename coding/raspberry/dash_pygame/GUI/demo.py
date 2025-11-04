import pygame
from GUI import widget


def run_widget_demo(widget_factory, window_size=(300, 300), title="Widget System Demo"):
    """
    Run a pygame demo for a widget.

    Args:
        widget_factory: function(font) -> list of widgets
        window_size: tuple (width, height) for pygame window
        title: window caption
    """
    pygame.init()
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption(title)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)  # font created AFTER pygame.init()

    widgets = widget_factory(font)

    running = True
    while running:
        screen.fill(widget.color_background)
        for w in widgets:
            w.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
