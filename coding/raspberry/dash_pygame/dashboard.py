import argparse


from dash_pygame.GUI.panel import Panel
from communication.mux_tx_rx import SerialManager
from communication.protocol import string_to_sensor_data
from camera.fake_picamera2 import Picamera2


def parse_args():
    parser = argparse.ArgumentParser(description="Dashboard")
    parser.add_argument("--simulate", "-s", action="store_true", help="Run in simulation (file-based) mode instead of real serial")
    parser.add_argument("--port", "-p", default="/dev/ttyACM0", help="Serial port to use when not simulating")
    parser.add_argument("--baud", "-b", type=int, default=19200, help="Baud rate for the serial connection")
    parser.add_argument("--debug", "-d", action="store_true", help="Debug mode?")
    parser.add_argument("--autodata", "-a", action="store_true", help="Automatic Data Generation?")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    
    picam2 = Picamera2()
    picam2.start()

    panel = Panel(args.autodata)

    sm = SerialManager(simulate=args.simulate, name='A', port=args.port, baud=args.baud, debug=args.debug)

    def on_receive(msg):
        sd = string_to_sensor_data(msg)

        # Update knobs
        for i, knob in enumerate(panel.knobs):
            knob.update_cur_val(sd.motor_encoders[i]*360/512)

        # Update sliders
        for i, slider in enumerate(panel.sliders):
            slider.update_cur_val(sd.motor_encoders[i+2]*360/512)  # slider maps to motor_encoders[2,3]
            
        # Update bars
        panel.bars[0].update_cur_val(sd.temp_sensor)
        panel.bars[1].update_cur_val(sd.ref_diode)

        # Update plotters
        for i, plotter in enumerate(panel.plotters):
            plotter.update_cur_val(sd.imu[i])
        

    sm.on_receive = on_receive
    sm.start()

    running = True
    counter = 0
    while running:
        frame = picam2.capture_array()
        panel.cambox[0].update_cur_val(frame)
        if counter%100 == 0:
            panel.logbox[0].update_cur_val(f"Counter: {counter}")
        counter += 1
        panel.handle_events()
        panel.draw()
        panel.tick()
