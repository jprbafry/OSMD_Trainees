import pygame
import argparse

from GUI import widget
from GUI.knob import Knob
from GUI.plotter import Plotter
from GUI.bar import Bar
from GUI.slider import Slider
from GUI.label import Label

from communication.mux_tx_rx import SerialManager
from ctypes import Structure, c_uint16, c_bool, c_float

# Sensor Data (structure using C types)
class SensorData(Structure):
    _fields_ = [
        ("motor_encoders", c_uint16 * 4),
        ("home_switches", c_bool * 4),
        ("potentiometers", c_uint16 * 2),
        ("ref_diode", c_uint16),
        ("temp_sensor", c_float),
        ("imu", c_float * 6)
    ]

# Decode comma-separated ASCII string
def string_to_sensor_data(msg: str) -> SensorData:
    parts = msg.split(",")
    sd = SensorData()
    sd.motor_encoders[:] = [int(parts[i]) for i in range(4)]
    sd.home_switches[:] = [bool(int(parts[i])) for i in range(4,8)]
    sd.potentiometers[:] = [int(parts[i]) for i in range(8,10)]
    sd.ref_diode = int(parts[10])
    sd.temp_sensor = float(parts[11])
    sd.imu[:] = [float(parts[i]) for i in range(12,18)]
    return sd

# Argument Parsing
def parse_args():
    parser = argparse.ArgumentParser(description="Motor Mockup (B) Serial Script")
    parser.add_argument("--simulate", "-s", action="store_true", help="Run in simulation (file-based) mode instead of real serial")
    parser.add_argument("--port", "-p", default="/dev/ttyACM0", help="Serial port to use when not simulating (e.g. /dev/ttyACM0)")
    parser.add_argument("--baud", "-b", type=int, default=19200, help="Baud rate for the serial connection")
    parser.add_argument("--debug", "-d", action="store_true", help="Debug mode?")
    return parser.parse_args()

if __name__ == "__main__":

    args = parse_args()
    
    # SerialManager Setup
    sm = SerialManager(simulate=args.simulate, name='A', port=args.port, baud=args.baud, debug=args.debug)

    # GUI Setup
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption("Widget System Demo + Bar")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    # Knobs
    knob_1 = Knob(150, 110, 60, 0, 360, font, auto=False)
    knob_2 = Knob(400, 110, 60, 0, 360, font, auto=False)

    # Plotters
    plotter_1 = Plotter(50, 250, 200, 100, 1, -1, (255,0,0), font, auto=False)
    plotter_2 = Plotter(50, 350, 200, 100, 1, -1, (0,255,0), font, auto=False)
    plotter_3 = Plotter(50, 450, 200, 100, 1, -1, (0,0,255), font, auto=False)
    plotter_4 = Plotter(300, 250, 200, 100, 1, -1, (255,255,0), font, auto=False)
    plotter_5 = Plotter(300, 350, 200, 100, 1, -1, (0,255,255), font, auto=False)
    plotter_6 = Plotter(300, 450, 200, 100, 1, -1, (255,0,255), font, auto=False)

    # Bars
    c_b1 = [(0, 0, 255), (255,255,255), (255, 0, 0)]
    c_b2 = [(255,255,255), (255, 165, 0)]
    bar_1 = Bar(550, 50, 30, 500, 0, 100, c_b1, "B 1", font, auto=False) 
    bar_2 = Bar(600, 50, 30, 500, 0, 1024, c_b2, "B 2", font, auto=False)

    widgets = [knob_1, knob_2, plotter_1, plotter_2, plotter_3, plotter_4, plotter_5, plotter_6, bar_1, bar_2]

    # COM updates
    def on_receive(msg):
        sd = string_to_sensor_data(msg)
        # HERE ... updating current values based on data sent through serial port
        knob_1.update_cur_val(sd.motor_encoders[0]*360/512)
        knob_2.update_cur_val(sd.motor_encoders[1]*360/512)
        bar_1.update_cur_val(sd.temp_sensor)
        bar_2.update_cur_val(sd.ref_diode)
        plotter_1.update_cur_val(sd.imu[0])
        plotter_2.update_cur_val(sd.imu[1])
        plotter_3.update_cur_val(sd.imu[2])
        plotter_4.update_cur_val(sd.imu[3])
        plotter_5.update_cur_val(sd.imu[4])
        plotter_6.update_cur_val(sd.imu[5])
    
    sm.on_receive = on_receive
    sm.start()


    # GUI Updates
    running = True
    while running:
        screen.fill(widget.color_background)
        for w in widgets:
            w.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
