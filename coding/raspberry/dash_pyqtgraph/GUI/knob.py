import numpy as np
import pyqtgraph as pg
from PyQt6.QtGui import QFont

from .widget import Widget, FONT_SIZE, BLACK, RED, BLUE

class Knob(Widget):
    """class to draw azimuthal rotation graphs"""
    def __init__(self, title, data, pos, size, x_range, y_range):
        super().__init__(title=title, data=data, pos=pos, size=size,
                         x_range=x_range, y_range=y_range)


    def draw(self, scene):
      angles = np.linspace(0, 2*np.pi, 360)
      x = np.cos(angles)
      y = np.sin(angles)
      p = pg.PlotItem(title=f"<span style='font-size:{FONT_SIZE}pt; color:{BLACK}'>Azimuthal Rotation ({self.title})</span>")

      # skeleton
      p.plot(x, y, pen=pg.mkPen(BLACK, width=2))
      p.setAspectLocked(True)
      p.setRange(xRange=self.x_range, yRange=self.y_range)
      p.hideAxis('left')
      p.hideAxis('bottom')

      # 0/360 degree markers
      zero_marker = pg.ScatterPlotItem([0.0], [1.0], symbol = 't', size=10, brush = BLACK)
      p.addItem(zero_marker)
      zero_text = pg.TextItem("0° / 360°", anchor=(0.5, 0), color = BLACK)
      p.addItem(zero_text)
      zero_text.setFont(QFont("Arial", FONT_SIZE))
      zero_text.setPos(0,1.5)

      # red dot
      self.dot = pg.ScatterPlotItem([1.0], [0.0], size=15, brush=RED, pen=pg.mkPen(BLUE, width=2))

      # angle text
      self.angle_text = pg.TextItem("0°", anchor=(0.5, 0.5), color=BLACK)
      p.addItem(self.dot)
      p.addItem(self.angle_text)
      self.angle_text.setFont(QFont("Arial", FONT_SIZE))
      self.angle_text.setPos(0,0)

      p.setPos(self.pos[0], self.pos[1])
      p.getViewBox().setFixedWidth(self.size[0])
      p.getViewBox().setFixedHeight(self.size[1])

      scene.addItem(p)


    def update(self, has_data):
        if has_data:
            raw_steps = int(self.data.motor_encoders[2]) if self.title == "Light Source" else int(self.data.motor_encoders[3])
            angle = raw_steps / 512 * 360
            rad = np.deg2rad(angle)
            # clockwise, swap sin/cos and invert y
            x = np.sin(rad)
            y = np.cos(rad)
            self.dot.setData([x], [y])
            self.angle_text.setText(f"{angle:.2f}°")
            self.angle_text.setPos(0, 0)
