# pylint: disable=line-too-long, import-error
"""This module draws the real-time dashboard of sensor data. Run with 'python drawer_mockup.py -n A'."""
import time
import argparse
import threading
import signal
import itertools
import logging
import inspect
from collections import deque

import pyqtgraph as pg
from PyQt6 import QtCore

from communication.mux_tx_rx import SerialManager
# from dash_pyqtgraph import GUI
from dash_pyqtgraph.GUI.knob import Knob
from dash_pyqtgraph.GUI.slider import Slider
from dash_pyqtgraph.GUI.button import Button
from dash_pyqtgraph.GUI.sinusoidal import Sinusoidal
from dash_pyqtgraph.GUI.color_bar import ColorBar
from dash_pyqtgraph.GUI.detector_window import DetectorWindow
from dash_pyqtgraph.GUI.log_window import LogWindow
from dash_pyqtgraph.GUI.widget import WHITE, BLACK, Q_SIZE, UPDATE_PERIOD, MAX_LOG_LEN
from dash_pyqtgraph.common import SensorDataPy

# setups for logging to console
console_logger = logging.getLogger("Dashboard")
console_logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
console_logger.addHandler(ch)
log_window_logger = logging.getLogger("log_window")

# sensor related variables
sd = SensorDataPy()

# other global variables
has_data = False
imu_queue_list = [deque([], Q_SIZE),
                  deque([], Q_SIZE),
                  deque([], Q_SIZE),
                  deque([], Q_SIZE),
                  deque([], Q_SIZE),
                  deque([], Q_SIZE),]
log_buffer = deque(maxlen = MAX_LOG_LEN)
counter = 0


def extract_data(sd, recv_msg):
    """function to extract data from the received msgs"""
    global counter, has_data
    if recv_msg is not None:
        has_data = True

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
        console_logger.info(log)
        log_window_logger.info(log)

    else:
        has_data = False
        log = f"No sensor data received: {sd}"
        console_logger.info(log)
        log_window_logger.info(log)

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


def draw_dashboard(scene, view, app):
    """function to draw the whole dashboard"""
    # allow ctrl + C to work while app.exec() is running
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    timer = QtCore.QTimer()
    update_functions = []

    # polar rotations (sliders)
    anchor_x = 50
    anchor_y = 50
    size_x = 200
    size_y = 150
    margin = 50
    cnt = 0
    for title in ["Light Source", "Detector"]:
        slider = Slider(title, sd,
                        [anchor_x, anchor_y + (size_y + margin) * cnt], [size_x, size_y],
                        [-20, 200], [0, 1])
        slider.draw(scene)
        update_functions.append(slider.update)
        cnt += 1

    # azimuthal rotations (knobs)
    anchor_x = 400
    anchor_y = 50
    cnt = 0
    for item in ["Light Source", "Detector"]:
        knob = Knob(item, sd,
                    [anchor_x, anchor_y + (size_y + margin) * cnt], [size_x, size_y],
                    [-1.2, 1.2], [-1.2,1.5])
        knob.draw(scene)
        update_functions.append(knob.update)
        cnt += 1

    # draw home switches (buttons)
    anchor_x = 80
    anchor_y = 480
    cnt = 0
    margin = 150
    # 4 combinations
    for pair in list(itertools.product(["Polar", "Azimuthal"], ["Light Source", "Detector"])):
        button = Button(pair, sd, [anchor_x + cnt * margin, anchor_y], [],
                        [], [])
        button.draw(scene)
        update_functions.append(button.update)
        cnt += 1

    # draw the imu (sinusoidal)
    anchor_x = 10
    anchor_y = 540
    size_x = 280
    size_y = 150
    margin = 40
    accelerator_plot = Sinusoidal("Accelerator", imu_queue_list,
                                  [anchor_x, anchor_y], [size_x, size_y],
                                  [], [-1, 1])
    gyroscope_plot = Sinusoidal("Gyroscope", imu_queue_list,
                                [anchor_x + size_x + margin, anchor_y], [size_x, size_y],
                                [], [-1, 1])
    accelerator_plot.draw(scene)
    gyroscope_plot.draw(scene)
    update_functions.append(accelerator_plot.update)
    update_functions.append(gyroscope_plot.update)

    # draw temperature and light (color gradient bars)
    anchor_x = 680
    anchor_y = 50
    size_x = 40
    size_y = 650
    margin = 60
    temp_bar = ColorBar("Temp", sd,
                        [anchor_x, anchor_y], [size_x, size_y],
                        [0, 1], [15, 17],)
    light_bar = ColorBar("Light", sd,
                         [anchor_x + margin, anchor_y], [size_x, size_y],
                         [0, 1], [0.8, 1.2])
    temp_bar.draw(scene)
    light_bar.draw(scene)
    update_functions.append(temp_bar.update)
    update_functions.append(light_bar.update)

    # detector feed
    anchor_x = 820
    anchor_y = 50
    size_x = 400
    size_y = 300
    detector_window = DetectorWindow("Detector Feed", None, [anchor_x, anchor_y], [size_x, size_y], [], [])
    detector_window.draw(scene)
    update_functions.append(detector_window.update)

    # debug info print to log window
    anchor_x = 820
    anchor_y = 420
    size_x = 400
    size_y = 300
    log_window = LogWindow("Logs", None, [anchor_x, anchor_y], [size_x, size_y], [], [])
    log_window.draw(scene, log_buffer)

    # connect update functions and start timer
    for fn in update_functions:
        n_params = len(inspect.signature(fn).parameters)
        if n_params == 1:
            timer.timeout.connect(lambda fn=fn: fn(has_data))
        if n_params == 2:
            timer.timeout.connect(lambda fn=fn: fn(has_data, imu_queue_list))

    timer.start(UPDATE_PERIOD)

    view.show()
    app.exec()


def main():
    """main"""
    # basic pyqtgraph setups
    pg.setConfigOptions(antialias=True)
    pg.setConfigOption('background', WHITE)   # white background
    pg.setConfigOption('foreground', BLACK)   # black axes/text
    app = pg.mkQApp("Dashboard")
    view = pg.GraphicsView()
    scene = pg.GraphicsScene()

    view.setScene(scene)
    view.setWindowTitle("Dashboard")
    view.resize(1260, 840)

    try:
        args = parse_args()

        # recv messages in another thread
        threads = [
            threading.Thread(target=recv_msgs, args=(args,), daemon=True),
        ]

        for t in threads:
            t.start()

        # draw in main thread
        draw_dashboard(scene, view, app)

    except KeyboardInterrupt:
        view.close()
        app.quit()


if __name__ == "__main__":
    main()
