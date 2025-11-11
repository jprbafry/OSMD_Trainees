import numpy as np
import matplotlib.pyplot as plt
import pyqtgraph as pg
from PyQt6.QtGui import QFont
from PyQt6 import QtCore

from .widget import Widget, FONT_SIZE, BLACK, WHITE

class Color_bar(Widget):
    def __init__(self, title, data, pos, size, x_range, y_range):
        super().__init__(title=title, data=data, pos=pos, size=size,
                         x_range=x_range, y_range=y_range)
    def draw(self):
        """function to draw the color gradient bar"""
        p = pg.PlotItem(title=f"<span style='font-size:{FONT_SIZE}pt; color:{BLACK}'>{self.title}</span>")
        p.hideAxis("left")
        p.hideAxis("bottom")
        num_points = 256
        p.setRange(xRange=self.x_range, yRange=self.y_range)
        gradient = np.linspace(self.y_range[0], self.y_range[1], num_points).reshape(-1, 1)
        gradient = np.flipud(gradient)
        gradient = np.rot90(gradient, k=-1)
        img = pg.ImageItem(gradient)
        # re-scale
        img.setRect(QtCore.QRectF(0, self.y_range[0], 1, self.y_range[1] - self.y_range[0]))

        if self.title == "Temp":
            cmap = plt.get_cmap('coolwarm')  # from Matplotlib
            lut = (cmap(np.linspace(0, 1, num_points))[:, :3] * (num_points - 1)).astype(np.uint8)  # RGB → 0–255
        else:
            cmap = plt.get_cmap('YlOrRd')  # from Matplotlib
            lut = (cmap(np.linspace(0, 1, num_points))[:, :3] * (num_points - 1)).astype(np.uint8)  # RGB → 0–255
        img.setLookupTable(lut)
        p.addItem(img)
        p.setPos(self.pos[0], self.pos[1])
        p.getViewBox().setFixedWidth(self.size[0])
        p.getViewBox().setFixedHeight(self.size[1])

        if self.title == "Temp":
            self.value_text = pg.TextItem("0°C", anchor=(0.5, 1.0), color = BLACK)
        else:
            self.value_text = pg.TextItem("0%", anchor=(0.5, 1.0), color = BLACK)

        # positioning of this value text is tricky, no good solution as of now
        # the PlotItem is shifted in scene space, so TextItem should also put in scene space
        bar_scene_x = self.pos[0] + self.size[0] / 2
        bar_scene_y = self.pos[1] + self.size[1] / 15
        self.value_text.setPos(bar_scene_x, bar_scene_y)

        # indicator
        self.indicator = pg.InfiniteLine(angle=0, pos=self.y_range[0], pen=pg.mkPen(WHITE, width = 4))
        self.border = pg.InfiniteLine(angle=0, pos=self.y_range[0], pen=pg.mkPen(BLACK, width = 6))
        p.addItem(self.border)
        p.addItem(self.indicator)
        return p, self.value_text
    
    def update(self):
        if self.title == "Temp":
            if self.data.temp_sensor != 0.0:
                self.indicator.setPos(self.data.temp_sensor)
                self.border.setPos(self.data.temp_sensor)
                self.value_text.setText(f"{self.data.temp_sensor: .2f}°C")
        else:
            if self.data.ref_diode != 0:
                # normalization
                ref_diode_base = 650
                value = self.data.ref_diode / ref_diode_base
                self.indicator.setPos(value)
                self.border.setPos(value)
                self.value_text.setText(f"{value * 100: .2f}%")
