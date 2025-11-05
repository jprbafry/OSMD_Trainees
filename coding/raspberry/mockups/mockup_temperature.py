import time
import argparse
import sys
import os
import math
import random


# Add the project root (raspberry/) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from communication import protocol 
 
#sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#from Bar import Bar
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from communication.mux_tx_rx import SerialManager

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
        #msg = f"{value:.2f}"
        
        sd = protocol.SensorData()
        sd.temp_sensor = float(f"{value:.2f}")
        print(f"Sent temperature: {sd.temp_sensor:.2f} °C")
        # Generate zero mock data for other fields
        sd.motor_encoders[:] = [0, 0, 0, 0]
        sd.home_switches[:] = [False, False, False, False]
        sd.potentiometers[:] = [0, 0]
        sd.ref_diode = 0
        sd.imu[:] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        msg = protocol.sensor_data_to_string(sd)
        sm.send(msg)

        if user_debug:
            print(f"[DEBUG] Sent temperature: {msg}")
        counter += 1 #how fast the temperature changes
        time.sleep(1) #send every 5 seconds

if __name__ == "__main__":
    args = parse_args()

    #create a SerialManager in simulated mode using fake serial files   
    sm = SerialManager(simulate=True, name=args.name, debug=False)
    #sm = SerialManager(port="/dev/ttyACM0", baud=19200 simulate=False, name=args.name, debug=False) # set simulate to False to use real serial port 
    user_debug = args.debug

    sm.start()   

try:
    mock_temperature_sender(sm)
except KeyboardInterrupt:
    print("\nCtrl+C pressed — stopping temperature sender")
    sm.stop()