

# ==========================
# === GLOBAL COLOR SCHEME ===
# ==========================
WHITE = "white"
BLACK = "black"
BLUE = "#4C72B0"
GREEN = "#55A868"
RED = "#C44E52"
GREY = "#E5E5E5"
DARK_GREY = "#4D4D4D"

FONT_SIZE = 12
Q_SIZE = 100

# ==========================
# === BASE WIDGET CLASS ===
# ==========================
class Widget:
    """Base class for all visual widgets"""
    def __init__(self, title, data, pos, size, x_range, y_range):
        self.title = title
        self.data = data
        self.pos = pos
        self.size = size
        self.x_range = x_range
        self.y_range = y_range

    def draw(self):
        pass

    def update(self, new_data = None):
        pass


