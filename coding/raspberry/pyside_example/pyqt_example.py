from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QDial, QSlider, QPushButton, QLabel
from PySide6.QtCore import Qt

app = QApplication([])

win = QWidget()
layout = QGridLayout(win)

# knob
for i in range(2):
  title = QLabel("Knob")
  title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
  # PySide positioning: row, row, row_expansion, column_expansion
  layout.addWidget(title, 2 * i, 2, 1, 2)

  knob = QDial()
  knob.setRange(30, 300)
  deg_label = QLabel("30°")
  deg_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
  deg_label.setAttribute(Qt.WA_TransparentForMouseEvents)
  knob.valueChanged.connect(lambda deg, deg_label = deg_label: deg_label.setText(f"{deg}°"))
  layout.addWidget(knob, 2 * i + 1, 2, 1, 2)
  layout.addWidget(deg_label, 2 * i + 1, 2, 1, 2)

# slider
for i in range(2):
  label = QLabel("Slider")
  label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
  layout.addWidget(label, 2 * i, 0, 2, 2)

  slider = QSlider(Qt.Horizontal)
  slider.setRange(0, 180)
  deg_label = QLabel("0°")
  deg_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
  deg_label.setAttribute(Qt.WA_TransparentForMouseEvents)
  slider.valueChanged.connect(lambda deg, deg_label = deg_label: deg_label.setText(f"{deg}°"))
  layout.addWidget(deg_label, 2 * i, 0, 2, 2)
  layout.addWidget(slider, 2 * i + 1, 0, 2, 2)

# button
for i in range(4):
  label = QLabel("Button")
  label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
  button = QPushButton("ON")
  layout.addWidget(label, 4, i, 1, 1)
  layout.addWidget(button, 5, i, 1, 1)

win.show()
app.exec()