# colors
WHITE = "white"
BLACK = "black"
BLUE = "#4C72B0"
GREEN = "#55A868"
RED = "#C44E52"
GREY = "#E5E5E5"
DARK_GREY = "#4D4D4D"

# other constants
Q_SIZE = 100
UPDATE_PERIOD = 100 # unit: ms
FONT_SIZE = 12
MAX_LOG_LEN = 10

# base class
class Widget:
    """Base class for all visual widgets"""
    def __init__(self, title, data, pos, size, x_range, y_range):
        self.title = title
        self.data = data
        self.pos = pos
        self.size = size
        self.x_range = x_range
        self.y_range = y_range

    def initialize(self):
        pass

    def draw(self, scene):
        pass

    def update(self, has_data, new_data = None):
        pass


