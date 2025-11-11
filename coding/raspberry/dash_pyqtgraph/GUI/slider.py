import pyqtgraph as pg
from PyQt6.QtGui import QFont

from .widget import Widget, FONT_SIZE, BLACK, RED, BLUE

class Slider(Widget):
    def __init__(self, title, data, pos, size, x_range, y_range):
        super().__init__(title=title, data=data, pos=pos, size=size,
                         x_range=x_range, y_range=y_range)


    def draw(self):
      """function to draw polar rotations"""
      global FONT_SIZE, BLACK, RED, BLUE
      self.p = pg.PlotItem(title=f"<span style='font-size:{FONT_SIZE}pt; color:{BLACK}'>Polar Rotation ({self.title})</span>")

      # Bbase line for the slider
      self.p.plot([0, 180], [0.5, 0.5], pen=pg.mkPen(BLACK, width=2))
      self.p.setAspectLocked(True)
      self.p.setRange(xRange=self.x_range, yRange=self.y_range)
      self.p.hideAxis('left')
      self.p.hideAxis('bottom')

      # moving red dot
      self.dot = pg.ScatterPlotItem([0], [0.5], size=15, brush=RED, pen=pg.mkPen(BLUE, width=2))
      self.p.addItem(self.dot)

      # angle text
      self.angle_text = pg.TextItem("0°", anchor=(0, 0), color=BLACK)
      self.angle_text.setFont(QFont("Arial", FONT_SIZE))
      self.angle_text.setPos(70, 40)
      self.p.addItem(self.angle_text)

      self.p.setPos(self.pos[0], self.pos[1])
      self.p.getViewBox().setFixedWidth(self.size[0])
      self.p.getViewBox().setFixedHeight(self.size[1])

      return self.p


    def update(self, has_data):
        """callback update function"""
        if has_data:
            raw_steps = int(self.data.motor_encoders[0]) if self.title == "Light Source" else int(self.data.motor_encoders[1])
            angle = raw_steps / 512 * 180
            self.dot.setData([angle], [0.5])
            self. angle_text.setText(f"{angle:.2f}°")
