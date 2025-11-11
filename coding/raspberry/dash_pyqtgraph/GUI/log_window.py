import logging

import pyqtgraph as pg
from PyQt6 import QtCore
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QTextEdit

from .widget import Widget, FONT_SIZE, BLACK, GREY, DARK_GREY

class QTextEditLogger(logging.Handler):
    """class for the logger piping the logs to the log widget"""
    def __init__(self, log_widget, log_buffer):
        super().__init__()
        self.log_widget = log_widget
        self.log_buffer = log_buffer

    def emit(self, record):
        msg = self.format(record)
        self.log_buffer.append(msg)
        # show
        QtCore.QMetaObject.invokeMethod(
            self.log_widget,
            "setPlainText",
            QtCore.Qt.ConnectionType.QueuedConnection,
            QtCore.Q_ARG(str, "\n".join(self.log_buffer))
        )
        # auto-scroll
        QtCore.QMetaObject.invokeMethod(
            self.log_widget.verticalScrollBar(),
            "setValue",
            QtCore.Qt.ConnectionType.QueuedConnection,
            QtCore.Q_ARG(int, self.log_widget.verticalScrollBar().maximum())
        )




class LogWindow(Widget):
    def __init__(self, title, data, pos, size, x_range, y_range):
        super().__init__(title=title, data=data, pos=pos, size=size,
                         x_range=x_range, y_range=y_range)


    def draw(self):
        """function to draw logging widget"""
        # title
        title = pg.TextItem(self.title, anchor=(0.5, 1), color=BLACK)
        title.setFont(QFont("Arial", FONT_SIZE))
        title.setPos(self.pos[0] + self.size[0] / 2, self.pos[1] - 5)

        # frame
        self.frame = pg.QtWidgets.QGraphicsRectItem(0, 0, self.size[0], self.size[1])
        self.frame.setPos(self.pos[0], self.pos[1])

        # log widget
        self.log_widget = QTextEdit()
        self.log_widget.setReadOnly(True)
        self.log_widget.setFixedSize(self.size[0], self.size[1])
        self.log_widget.setStyleSheet(f"""
        QTextEdit {{
            background-color: {GREY};
            border: 1px solid {DARK_GREY};
            font-family: Consolas, monospace;
            font-self.size: {FONT_SIZE}pt;
            color: {BLACK};
        }}
        """)

        return self.frame, self.log_widget


    def initialize(self, log_proxy, log_handler):
        log_proxy.setParentItem(self.frame)

        # connect logger with the log widget
        log_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", "%H:%M:%S"))
        logging.getLogger().addHandler(log_handler)
