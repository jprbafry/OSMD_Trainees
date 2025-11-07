import time
import math
import random
import threading
import argparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from communication import protocol
from communication.mux_tx_rx import SerialManager


def parse_args():
    parser = argparse.ArgumentParser(description="Threaded IMU mockup sender (accelerometer + gyroscope)")
    parser.add_argument("--name", "-n", choices=["A", "B"], required=True,
                        help="Simulation node name (A = sender, B = receiver)")
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debug logs")
    parser.add_argument("--period", "-p", type=int, default=50, help="Send period in ms")
    return parser.parse_args()

# Thread: continuously update IMU data

def update_imu(sd: protocol.SensorData, lock: threading.Lock, period_ms=20):
    start_time = time.time()
    phases = [0, math.pi/3, 2*math.pi/3, math.pi, 4*math.pi/3, 5*math.pi/3]
    freqs = [random.uniform(1,5) for _ in range(6)]
    amplitude = 1.0
    while True:
        with lock:
            t = time.time() - start_time
            for i in range(6):
                sd.imu[i] = amplitude * math.sin(freqs[i]*t + phases[i])
        time.sleep(period_ms / 1000)


        time.sleep(period_ms / 1000.0)  # update frequency (~50 Hz)


# Main: send updated IMU data

def mock_imu_sender(sm: SerialManager, user_debug=False, period_ms=50):
    """
    Continuously send IMU data through SerialManager,
    while the IMU values are updated by a background thread.
    """
    sd = protocol.SensorData()
    lock = threading.Lock()

    # Initialize all fields
    sd.temp_sensor = 0.0
    sd.motor_encoders[:] = [0, 0, 0, 0]
    sd.home_switches[:] = [False, False, False, False]
    sd.potentiometers[:] = [0, 0]
    sd.ref_diode = 0
    sd.imu[:] = [0.0] * 6

    # Start IMU update thread
    threading.Thread(target=update_imu, args=(sd, lock, period_ms), daemon=True).start()

    while sm.running.is_set():
        with lock:
            msg = protocol.sensor_data_to_string(sd)

        sm.send(msg)

        if user_debug:
            with lock:
                imu_str = ", ".join(f"{v:.3f}" for v in sd.imu)
                print(f"Sent IMU: {imu_str}")

        time.sleep(period_ms / 1000.0)

if __name__ == "__main__":
    args = parse_args()
    sm = SerialManager(simulate=True, name=args.name, debug=args.debug)
    user_debug = args.debug

    sm.start()
    
    try:
        mock_imu_sender(sm, user_debug=user_debug, period_ms=args.period)
    except KeyboardInterrupt:
        print("\nCtrl+C pressed — stopping IMU sender")
        sm.stop()
