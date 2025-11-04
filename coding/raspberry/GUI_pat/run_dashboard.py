import argparse
import sys, os
from dashboard import Dashboard #import the Dashboard class

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #add parent directory to path
from mux_tx_rx import SerialManager #import SerialManager for serial communication

#Argument parser for command-line options
def parse_args():
    parser = argparse.ArgumentParser(description="ControlParameters")
    parser.add_argument("--simulate", "-s", action="store_true", help="Run in simulation (file-based) mode instead of real serial")
    parser.add_argument("--port", "-p", default="/dev/ttyACM0", help="Serial port to use when not simulating (e.g. /dev/ttyACM0)")
    parser.add_argument("--baud", "-b", type=int, default=19200, help="Baud rate for the serial connection")
    parser.add_argument("--debug", "-d", action="store_true", help="Debug mode?")
    return parser.parse_args()

#Callback function for received serial messages
def on_receive(msg):
    print(msg)
    dashboard.update_temperature(float(msg.split(",")[0]))

#Main
if __name__ == "__main__":
    args = parse_args()

    dashboard = Dashboard() #Create Dashboard instance

    #Create SerialManager (node B)
    sm = SerialManager(
        simulate=args.simulate,
        name="B",
        port=args.port,
        baud=args.baud,
        debug=args.debug
    )

    sm.on_receive = on_receive #Set callback for received messages
    sm.start() #Start SerialManager
    dashboard.run() #Run the dashboard
