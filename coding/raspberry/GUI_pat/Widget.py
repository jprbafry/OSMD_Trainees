# ==========================
# === GLOBAL COLOR SCHEME ===
# ==========================
color_desired = (255, 0, 0)      # red
color_current = (0, 255, 0)      # green
color_text = (255, 255, 255)     # white
color_background = (10, 10, 10)  # dark grey
color_line = (150, 150, 150)     # grey
color_button_busy = (255, 255, 0)  # yellow
color_button_idle = (255, 255, 255)  # white

# ==========================
# === BASE WIDGET CLASS ===
# ==========================
class Widget:
    """Base class for all visual widgets"""
    def __init__(self, x, y, width=0, height=0, min_val=0, max_val=100):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.cur_val = (max_val-min_val)/2
        self.visible = True

    def update_cur_val(self):
        pass

    def draw(self, surface):
        pass

    def __generate_own_data(self):
        pass