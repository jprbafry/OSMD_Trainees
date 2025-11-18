
import argparse
from dash_pygame.GUI.panel import Panel

from communication.mux_tx_rx import SerialManager

def parse_args():
    parser = argparse.ArgumentParser(description="Dashboard")
    parser.add_argument("--simulate", "-s", action="store_true", help="Run in simulation (file-based) mode instead of real serial")
    parser.add_argument("--port", "-p", default="/dev/ttyACM0", help="Serial port to use when not simulating")
    parser.add_argument("--baud", "-b", type=int, default=115200, help="Baud rate for the serial connection")
    parser.add_argument("--debug", "-d", action="store_true", help="Debug mode?")
    parser.add_argument("--autodata", "-a", action="store_true", help="Automatic Data Generation?")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    panel = Panel(args.autodata)

    sm = SerialManager(simulate=args.simulate, name='A', port=args.port, baud=args.baud, debug=args.debug)

    def on_receive():
        sensors = sm.msgManagerReceive.data

       # print(f"motor encoders: {sensors['motor_encoders'][0]}, {sensors['motor_encoders'][1]}, {sensors['motor_encoders'][2]}, {sensors['motor_encoders'][3]}")
       # print(f"home switches: {sensors['home_switches'][0]}, {sensors['home_switches'][1]}, {sensors['home_switches'][2]}, {sensors['home_switches'][3]}")
       # print(f"potentiometers: {sensors['potentiometers'][0]}, {sensors['potentiometers'][1]}")
       # print(f"ref diode: {sensors['ref_diode'][0]}, temperature: {sensors['temp_sensor'][0]}")
        print(f"imu: {sensors['imu'][0]}, {sensors['imu'][1]}, {sensors['imu'][2]}, {sensors['imu'][3]}, {sensors['imu'][4]}, {sensors['imu'][5]}")

        try:
            panel.bars[0].update_cur_val(sensors['temp_sensor'][0])
            panel.bars[1].update_cur_val(sensors['ref_diode'][0])

            for i, plotter in enumerate(panel.plotters):
                plotter.update_cur_val(sensors['imu'][i])
        except Exception as e:
            print(f"Error updating dashboard: {e}")
        
    sm.on_receive = on_receive
    sm.start()

    running = True
    while running:
        panel.draw()
        panel.tick()
