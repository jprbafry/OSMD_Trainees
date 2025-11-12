import numpy as np
import pyqtgraph as pg
import cv2

from .widget import Widget, FONT_SIZE, BLACK
from .demo import run_widget_demo


class DetectorWindow(Widget):
    """function to draw the feed from the camera/detector"""
    def __init__(self, title, data, pos, size, x_range, y_range):
        super().__init__(title=title, data=data, pos=pos, size=size,
                         x_range=x_range, y_range=y_range)


    def draw(self, scene):
        p = pg.PlotItem(title=f"<span style='font-size:{FONT_SIZE}pt; color:{BLACK}'>{self.title}</span>")
        p.hideAxis("left")
        p.hideAxis("bottom")
        p.setPos(self.pos[0], self.pos[1])
        p.getViewBox().setFixedWidth(self.size[0])
        p.getViewBox().setFixedHeight(self.size[1])

        self.img = pg.ImageItem()
        p.addItem(self.img)
        # TODO: replace this local video file with real detector feed
        self.video_path = cv2.samples.findFile("./dash_pyqtgraph/GUI/tree.avi")
        self.capture = None

        scene.addItem(p)


    def update(self, has_data):
        if has_data:
            if self.capture is None:
                self.capture = cv2.VideoCapture(self.video_path)
            ret, frame = self.capture.read()
            if not ret:
                self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)  # loop
                ret, frame = self.capture.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame, 3)
            self.img.setImage(frame, autoLevels = False)
        else:
            self.capture = None


def main():
    """Entry for standalone demo"""
    anchor_x = 20
    anchor_y = 20
    size_x = 320
    size_y = 240

    detector_window = DetectorWindow("Detector Feed", None, [anchor_x, anchor_y], [size_x, size_y], [], [])

    run_widget_demo(detector_window.draw, detector_window.update)


if __name__ == "__main__":
    main()