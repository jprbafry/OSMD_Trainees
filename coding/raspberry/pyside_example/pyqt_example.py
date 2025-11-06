from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QDial, QSlider, QPushButton

app = QApplication([])

win = QWidget()
layout = QGridLayout(win)

dial = QDial()
slider = QSlider()
button = QPushButton("OK")

layout.addWidget(dial, 0, 0)
layout.addWidget(slider, 0, 0)
# row=1, col=0, span 2 columns
layout.addWidget(button, 1, 0, 1, 2)

win.show()
app.exec()