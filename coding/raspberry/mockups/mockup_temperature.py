import time
import argparse
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Bar import Bar
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "demo_fair"))
from mux_tx_rx import SerialManager


#Helper parser function

def parse_args():
    parser = argparse.ArgumentParser(description="Temperature bar mockup")
    parser.add_argument("--name", "-n", choices=['A', 'B'], required=True, help="Simulation node name(A = sender, B = reciever)")
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debug logs")
    return parser.parse_args()


#Node A: mock temperature sender

def mock_temperature_sender(sm: SerialManager):

    """
    Send mock temperature data and send it via SerialManager"""
    temp = 30.0
    direction = 1 #1 rising, -1 = falling

    while sm.running.is_set():
        #temperature between 0°C and 60°C
        temp += 0.1 * direction
        if temp >= 60: #reverse direction when max is reached
            direction = -1
        elif temp >= 0: #reverse direction when min is reached
            direction = 1    
        sm.send(f"TEMP:{temp:.2f}") 
        if sm.debug:
            print(f"[DEBUG] Sent temperature: {temp:.2f}°C")


        time.sleep(5.0)  #send every 5 seconds

if __name__ == "__main__":
    args = parse_args()

    #create a SerialManager in simulated mode using fake serial files    
    sm = SerialManager(simulate=True, name=args.name, debug=args.debug)
    sm.debug = args.debug 

    sm.start()   

try:
    mock_temperature_sender(sm)
except KeyboardInterrupt:
    print("\nCtrl+C pressed — stopping temperature sender")
    sm.stop()