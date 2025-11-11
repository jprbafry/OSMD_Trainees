import numpy as np
import pyqtgraph as pg
from PyQt6.QtGui import QFont

from .widget import Widget, FONT_SIZE, BLACK, RED, BLUE, GREEN, Q_SIZE

class Sinusoidal(Widget):
    """class to draw imu graphs (3 graphs in one plot)"""
    def __init__(self, title, data, pos, size, x_range, y_range):
        super().__init__(title=title, data=data, pos=pos, size=size,
                         x_range=x_range, y_range=y_range)


    def draw(self):
        self.item_no = 0 if self.title == "Accelerator" else 3
        self.p = pg.PlotItem(title=f"<span style='font-size:{FONT_SIZE}pt; color:{BLACK}'>{self.title}</span>")
        legend = self.p.addLegend()
        legend.anchor(itemPos=(1,0), parentPos=(1,0), offset=(10,-10))
        legend.setBrush(pg.mkBrush('w'))

        # Only show data from last 0.1s
        self.window = Q_SIZE
        self.last_item = []
        self.colors = [BLUE, GREEN, RED]
        self.names = ["x", "y", "z"]
        for i in range(0,3):
            self.last_item.append(self.p.plot(list(self.data[i + self.item_no])[i:self.window], pen=pg.mkPen(self.colors[i], width=2), name = self.names[i]))
        self.p.setRange(xRange=[0, self.window], yRange=self.y_range)

        self.p.setPos(self.pos[0], self.pos[1])
        self.p.getViewBox().setFixedWidth(self.size[0])
        self.p.getViewBox().setFixedHeight(self.size[1])

        return self.p


    def update(self, has_data, new_data):
        if has_data:
            self.data = new_data
            for item in self.last_item:
                self.p.removeItem(item)

            for i in range(0,3):
                self.last_item[i] = self.p.plot(list(self.data[i + self.item_no])[i:self.window], pen=pg.mkPen(self.colors[i], width=2), name = self.names[i])
