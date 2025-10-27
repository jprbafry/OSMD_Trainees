import time
import argparse
import sys
import os
import math
import random


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
    #Send mock temperature data and send it via SerialManager
    counter = 0.0
  

    while sm.running.is_set(): #Block that sends mock temp data
        value = 16 + 8 * math.sin(counter) #oscillates between 8°C and 24°C
        msg = f"{value:.2f}"
        sm.send(msg)

        if user_debug:
            print(f"[DEBUG] Sent temperature: {msg}")
        counter += 1 #controls the sine wave frequency
        time.sleep(5) #send every 5 seconds



        # #temperature between 0°C and 60°C
        # temp += 0.1 * direction
        # if temp >= 60: #reverse direction when max is reached
        #     direction = -1
        # elif temp >= 0: #reverse direction when min is reached
        #     direction = 1    
        # sm.send(f"TEMP:{temp:.2f}") 
        # if user_debug:
        #     print(f"[DEBUG] Sent temperature: {temp:.2f}°C")


        # time.sleep(5.0)  #send every 5 seconds

if __name__ == "__main__":
    args = parse_args()

    #create a SerialManager in simulated mode using fake serial files    
    sm = SerialManager(simulate=True, name=args.name, debug=False)
    user_debug = args.debug

    sm.start()   

try:
    mock_temperature_sender(sm)
except KeyboardInterrupt:
    print("\nCtrl+C pressed — stopping temperature sender")
    sm.stop()