import pyqtgraph as pg
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton

from .widget import Widget, FONT_SIZE, BLACK, WHITE, GREY, GREEN
from .demo import run_widget_demo
from dash_pyqtgraph.common import SensorDataPy


class Button(Widget):
    """class to draw home switches"""
    def __init__(self, title, data, pos, size, x_range, y_range):
        super().__init__(title=title, data=data, pos=pos, size=size,
                         x_range=x_range, y_range=y_range)


    def draw(self, scene):
        rotation = self.title[0]
        device = self.title[1]
        self.item_no = 0 if device == "Light Source" else 1
        self.item_no = self.item_no if rotation == "Polar" else self.item_no + 2
        self.button = QPushButton("OFF")
        # make it a toggle button
        self.button.setCheckable(True)
        self.button.setFlat(True)
        self.button.setStyleSheet(f"""
            QPushButton {{
                background-color: {GREY};
                color: {BLACK};
                padding: 5px 15px;
            }}
            QPushButton:checked {{
                background-color: {GREEN};
                color: {WHITE};
                padding: 5px 15px;
            }}
        """)
        title_label = pg.TextItem(f"{device}\n{rotation}", anchor=(0.5, 0.5), color=BLACK)
        title_label.setFont(QFont("Arial", FONT_SIZE))
        title_label.setPos(self.pos[0] + 30, self.pos[1] - 20)

        btn_proxy = scene.addWidget(self.button)
        btn_proxy.setPos(self.pos[0], self.pos[1])
        scene.addItem(title_label)


    def update(self, has_data):
        if has_data:
            checked = self.data.home_switches[self.item_no]
            self.button.setChecked(checked)
            self.button.setText("ON" if checked else "OFF")


def main():
    """Entry for standalone demo"""
    sd = SensorDataPy()
    sd.home_switches[0] = 1
    anchor_x = 80
    anchor_y = 80
    button = Button(("Polar", "Light Source"), sd,
                    [anchor_x, anchor_y], [],
                    [], [])
    # update once
    run_widget_demo(button.draw, button.update)

if __name__ == "__main__":
    main()