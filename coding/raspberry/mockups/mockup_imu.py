import time
import argparse
import sys
import os
import math
import random


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#from dash_pygame.communication import protocol
from mux_tx_rx import SerialManager

# ----------------------------------------
# Parse arugments
# ----------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="IMU mockup sender (accelerometer + gyroscope)")
    parser.add_argument("--name", "-n", choices=['A', 'B'], required=True, help="Simulation node name (A = sender, B = receiver)")
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debug logs")
    return parser.parse_args()


# ----------------------------------------
# Mock IMU Sender (Node A)
# ----------------------------------------
def mock_imu_sender(sm: SerialManager, debug=False):
    """
    Continuously send simulated IMU data (accelerometer + gyroscope)
    through SerialManager.
    """
    counter = 0.0

    while sm.running.is_set():
        # --- Generate smooth pseudo-IMU data ---
        ax = round(1.0 * math.sin(counter / 10.0) + random.uniform(-0.05, 0.05), 3)
        ay = round(1.0 * math.cos(counter / 10.0) + random.uniform(-0.05, 0.05), 3)
        az = round(9.81 + random.uniform(-0.1, 0.1), 3)  # gravity component

        gx = round(0.5 * math.sin(counter / 15.0) + random.uniform(-0.02, 0.02), 3)
        gy = round(0.5 * math.cos(counter / 15.0) + random.uniform(-0.02, 0.02), 3)
        gz = round(random.uniform(-0.05, 0.05), 3)

        msg = f"{ax},{ay},{az},{gx},{gy},{gz}"

        sm.send(msg)

        if debug:
            print(f"Sent IMU: {msg}")

        counter += 1
        time.sleep(1.0)  # send every 1 second


#To test the mockup IMU sender
if __name__ == "__main__":
    args = parse_args()

    # Create SerialManager in simulated mode
    sm = SerialManager(simulate=False, name=args.name, debug=args.debug)
    sm.start()

    try:
        mock_imu_sender(sm, debug=args.debug)
    except KeyboardInterrupt:
        print("\nCtrl+C pressed — stopping IMU sender")
        sm.stop()
