from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QDial, QSlider, QPushButton
from PySide6.QtCore import Qt

app = QApplication([])

win = QWidget()
layout = QGridLayout(win)


for i in range(2):
  knob = QDial()

  layout.addWidget(knob, 2 * i + 1, 2, 1, 2)

for i in range(2):
  slider = QSlider(Qt.Horizontal)
  layout.addWidget(slider, 2 * i + 1, 0, 2, 2)

for i in range(4):
  button = QPushButton("OK")
  layout.addWidget(button, 4, i, 1, 1)

win.show()
app.exec()