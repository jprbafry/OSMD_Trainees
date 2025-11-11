# pylint: disable=line-too-long, import-error
"""This module draws the real-time dashboard of sensor data. Run with 'python drawer_mockup.py -n A'."""
import sys
import time
import argparse
import threading
from dataclasses import dataclass
import signal
import itertools
import logging
from collections import deque
from functools import partial
import inspect
from PyQt6 import QtCore

from PyQt6.QtWidgets import QPushButton, QTextEdit
import pyqtgraph as pg

from communication.mux_tx_rx import SerialManager
import dash_pyqtgraph.GUI as GUI

# colors
WHITE = "white"
BLACK = "black"

# other constants
Q_SIZE = 100
UPDATE_PERIOD = 100 # unit: ms
FONT_SIZE = 12
MAX_LOG_LEN = 10

# global variables
data_feed = False
pg.setConfigOptions(antialias=True)
pg.setConfigOption('background', WHITE)   # white background
pg.setConfigOption('foreground', BLACK)   # black axes/text
app = pg.mkQApp("Dashboard")
view = pg.GraphicsView()
scene = pg.GraphicsScene()
imu_queue_list = [deque([], Q_SIZE),
                  deque([], Q_SIZE),
                  deque([], Q_SIZE),
                  deque([], Q_SIZE),
                  deque([], Q_SIZE),
                  deque([], Q_SIZE),]
counter = 0
log_buffer = deque(maxlen = MAX_LOG_LEN)

# setups for logging to console
logger = logging.getLogger("Dashboard")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
logger.addHandler(ch)


@dataclass
class SensorDataPy:
    """data class for Python (Raspberry) side"""
    motor_encoders: list[int]
    home_switches: list[bool]
    potentiometers: list[int]
    ref_diode: int
    temp_sensor: float
    imu: list[float]
sd = SensorDataPy([0,0,0,0],
                  [False, False, False, False],
                  [0,0],
                  0, 0.0,
                  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
update_functions = []


def extract_data(sd, recv_msg):
    """function to extract data from the received msgs"""
    global counter, data_feed
    if recv_msg is not None:
        data_feed = True

        offset = 0
        msg = recv_msg.split(",")
        for i in range(0,4):
            sd.motor_encoders[i] = int(msg[i])

        offset = 4
        for i in range(4,8):
            sd.home_switches[i - offset] = True if msg[i] == "1" else False

        offset = 8
        for i in range(8,10):
            sd.potentiometers[i - offset] = int(msg[i])

        sd.ref_diode = int(msg[10])
        sd.temp_sensor = float(msg[11])

        offset = 12
        for i in range(12,18):
            sd.imu[i - offset] = float(msg[i])
            imu_queue_list[i - offset].append(float(msg[i]))

        counter += 1
        log = f"{counter} Received sensor data: {sd}"
        logger.info(log)
        log_buffer.append(log)

    else:
        data_feed = False
        log = f"No sensor data received: {sd}"
        logger.info(log)
        log_buffer.append(log)


def parse_args():
    """function to parse arguments, used in main()"""
    parser = argparse.ArgumentParser(description="Motor Mockup (B) Serial Script")
    parser.add_argument("--simulate", "-s", action="store_true", help="Run in simulation (file-based) mode instead of real serial")
    parser.add_argument("--port", "-p",default="/dev/ttyACM0", help="Serial port to use when not simulating (e.g. /dev/ttyACM0)")
    parser.add_argument("--baud", "-b",type=int, default=38400, help="Baud rate for the serial connection")
    parser.add_argument("--debug", "-d", action="store_true", help="Debug mode?")
    parser.add_argument("--name", "-n", choices=['A', 'B'], required=True, help="Name of this node (A or B) for simulation mode")
    return parser.parse_args()


def recv_msgs(args):
    """function to receive messages from the server"""
    sm = SerialManager(simulate=args.simulate, port=args.port, baud=args.baud, name=args.name)
    sm.start()
    try:
        while True:
            received_msg = sm.recv()
            extract_data(sd, received_msg)
            time.sleep(UPDATE_PERIOD / 1000)
    except KeyboardInterrupt:
        print(f"Ctrl+C pressed — stopping {args.name}")
        sm.stop()


def draw_dashboard():
    """function to draw the whole dashboard"""
    view.setScene(scene)
    view.setWindowTitle("Dashboard")
    view.resize(1260, 840)

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    timer = QtCore.QTimer()

    # polar rotations (sliders)
    anchor_x = 50
    anchor_y = 50
    size_x = 200
    size_y = 150
    margin = 50
    cnt = 0
    for title in ["Light Source", "Detector"]:
        slider = GUI.Slider(title, sd,
                        [anchor_x, anchor_y + (size_y + margin) * cnt], [size_x, size_y],
            [-20, 200], [0, 1])
        scene.addItem(slider.draw())
        update_functions.append(slider.update)
        cnt += 1

    # azimuthal rotations (knobs)
    anchor_x = 400
    anchor_y = 50
    cnt = 0
    for item in ["Light Source", "Detector"]:
        knob = GUI.Knob(item, sd,
                    [anchor_x, anchor_y + (size_y + margin) * cnt], [size_x, size_y],
                    [-1.2, 1.2], [-1.2,1.5])
        scene.addItem(knob.draw())
        update_functions.append(knob.update)
        cnt += 1

    # draw home switches (buttons)
    anchor_x = 80
    anchor_y = 480
    cnt = 0
    margin = 150
    # 4 combinations
    for pair in list(itertools.product(["Polar", "Azimuthal"], ["Light Source", "Detector"])):
        button = GUI.Button(pair, sd, [anchor_x + cnt * margin, anchor_y], [],
                            [], [])
        items = button.draw()
        btn_proxy = scene.addWidget(items[0])
        scene.addItem(items[1])
        button.initialize(btn_proxy)
        update_functions.append(button.update)
        cnt += 1

    # draw the imu (sinusoidal)
    anchor_x = 10
    anchor_y = 540
    size_x = 280
    size_y = 150
    margin = 40
    accelerator_plot = GUI.Sinusoidal("Accelerator", imu_queue_list,
                                      [anchor_x, anchor_y], [size_x, size_y],
                                      [], [-1, 1])
    gyroscope_plot = GUI.Sinusoidal("Gyroscope", imu_queue_list,
                                    [anchor_x + size_x + margin, anchor_y], [size_x, size_y],
                                    [], [-1, 1])
    scene.addItem(accelerator_plot.draw())
    scene.addItem(gyroscope_plot.draw())
    timer.timeout.connect(partial(accelerator_plot.update, imu_queue_list))
    timer.timeout.connect(partial(gyroscope_plot.update, imu_queue_list))

    # draw temperature and light (color gradient bars)
    anchor_x = 680
    anchor_y = 50
    size_x = 40
    size_y = 650
    margin = 60
    temp_bar = GUI.Color_bar("Temp", sd,
                         [anchor_x, anchor_y], [size_x, size_y],
                         [0, 1], [15, 17],)
    light_bar = GUI.Color_bar("Light", sd,
                          [anchor_x + margin, anchor_y], [size_x, size_y],
                          [0, 1], [0.8, 1.2])
    item_list = []
    item_list.extend(temp_bar.draw())
    item_list.extend(light_bar.draw())

    for item in item_list:
        scene.addItem(item)

    update_functions.append(temp_bar.update)
    update_functions.append(light_bar.update)

    # detector feed
    detector_window = GUI.Detector_window("Detector Feed", None, [820, 50], [400, 300], [], [])
    scene.addItem(detector_window.draw())
    update_functions.append(scene.update)

    # debug info
    log_window = GUI.Log_window("Logs", None, [820, 420], [400, 300], [], [])
    frame, log_widget = log_window.draw()
    scene.addItem(frame)
    log_proxy = scene.addWidget(log_widget)
    log_handler = GUI.QTextEditLogger(log_widget, log_buffer)
    log_window.initialize(log_proxy, log_handler)

    # allow ctrl + C to work while app.exec() is running
    for fn in update_functions:
        timer.timeout.connect(fn)
        
    timer.start(UPDATE_PERIOD)

    view.show()
    app.exec()


def main():
    """main"""
    try:
        args = parse_args()

        # recv messages in another thread
        threads = [
            threading.Thread(target=recv_msgs, args=(args,), daemon=True),
        ]

        for t in threads:
            t.start()

        # draw in main thread
        draw_dashboard()

    except KeyboardInterrupt:
        view.close()
        app.quit()


if __name__ == "__main__":
    main()
