import argparse


from dash_pygame.GUI.panel import Panel
from communication.mux_tx_rx import SerialManager
from communication.protocol import string_to_sensor_data
from ComsModule import MessageManager


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
    panel = Panel(args.autodata)

    sm = SerialManager(simulate=args.simulate, name='A', port=args.port, baud=args.baud, debug=args.debug)

    def on_receive(msgmanager):
        #sd = string_to_sensor_data(msg)

        # Update bars
        #panel.bars[0].update_cur_val(sd.temp_sensor)
        #panel.bars[1].update_cur_val(sd.ref_diode)

        sensors = msgmanager.getSensors()

        print(f"Value of temp sensor: {sensors.temp_sensor}")
        print(f"Value of ref diode: {sensors.ref_diode}")

        panel.bars[0].update_cur_val(sensors.temp_sensor)
        panel.bars[1].update_cur_val(sensors.ref_diode)

        # Update plotters
        for i, plotter in enumerate(panel.plotters):
            #plotter.update_cur_val(sd.imu[i])

            plotter.update_cur_val(sensors.imu[i])

    sm.on_receive = on_receive
    sm.start()

    running = True
    while running:
        panel.draw()
        panel.tick()
