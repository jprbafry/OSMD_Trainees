import threading
import time
import math
import random
import os
import argparse
from ctypes import Structure, c_uint16, c_bool, c_float
from mux_tx_rx import SerialManager

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

# Function to put data into a single string
def sensor_data_to_string(sensor: SensorData) -> str:
    values = []
    values.extend(sensor.motor_encoders[:])
    values.extend(int(b) for b in sensor.home_switches[:])
    values.extend(sensor.potentiometers[:])
    values.append(sensor.ref_diode)
    values.append(f"{sensor.temp_sensor:.3f}")
    values.extend(f"{v:.3f}" for v in sensor.imu[:])
    return ",".join(str(v) for v in values)






# Function to update motor encoders data
def update_motor_encoders(sd: SensorData, lock: threading.Lock, step=1, period_ms=20):
    direction = [1]*4
    while True:
        with lock:
            for i in range(4):
                sd.motor_encoders[i] += direction[i]*step
                if sd.motor_encoders[i] >= 511:
                    sd.motor_encoders[i] = 511
                    direction[i] = -1
                elif sd.motor_encoders[i] <= 0:
                    sd.motor_encoders[i] = 0
                    direction[i] = 1
        time.sleep(period_ms / 1000)

# Function to update Homing sensors data
def update_home_switches(sd: SensorData, lock: threading.Lock, period_ms=40):
    while True:
        with lock:
            for i in range(4):
                sd.home_switches[i] = (sd.motor_encoders[i] < 5)
        time.sleep(period_ms / 1000)

# Function to update Potentiometers data
def update_potentiometers(sd: SensorData, lock: threading.Lock, period_ms=40):
    while True:
        with lock:
            sd.potentiometers[0] = sd.motor_encoders[2]
            sd.potentiometers[1] = sd.motor_encoders[3]
        time.sleep(period_ms / 1000)

# Function to update Reference Diode data
def update_ref_diode(sd: SensorData, lock: threading.Lock, period_ms=100):
    while True:
        with lock:
            sd.ref_diode = 650 + random.randint(-20,20)
        time.sleep(period_ms / 1000)

# Function to update Temperature data
def update_temperature(sd: SensorData, lock: threading.Lock, period_ms=200):
    start_time = time.time()
    while True:
        with lock:
            t = time.time() - start_time
            sd.temp_sensor = 16 + 8 * math.sin(2*math.pi * t / (24*60*60))
        time.sleep(period_ms / 1000)

# Function to update IMU data
def update_imu(sd: SensorData, lock: threading.Lock, period_ms=40):
    start_time = time.time()
    phases = [0, math.pi/3, 2*math.pi/3, math.pi, 4*math.pi/3, 5*math.pi/3]
    amplitude = 1.0
    freq = 0.5
    while True:
        with lock:
            t = time.time() - start_time
            for i in range(6):
                sd.imu[i] = amplitude * math.sin(2*math.pi*freq*t + phases[i])
        time.sleep(period_ms / 1000)





# Argument Parsing
def parse_args():
    parser = argparse.ArgumentParser(description="Motor Mockup (B) Serial Script")
    parser.add_argument("--simulate", "-s", action="store_true", help="Run in simulation (file-based) mode instead of real serial")
    parser.add_argument("--port", "-p", default="/dev/ttyACM0", help="Serial port to use when not simulating (e.g. /dev/ttyACM0)")
    parser.add_argument("--baud", "-b", type=int, default=19200, help="Baud rate for the serial connection")
    parser.add_argument("--debug", "-d", action="store_true", help="Debug mode?")
    return parser.parse_args()






# Main function
if __name__ == "__main__":

    args = parse_args()

    # Serial manager
    sm = SerialManager(simulate=args.simulate, name='B', port=args.port,
                       baud=args.baud, debug=args.debug)
    sm.start()

    # SensorData instance
    sd = SensorData()

    # Initialization of Sensor Data
    sd.motor_encoders[:] = [511, 255, 127, 63]
    sd.home_switches[:] = [False, False, False, False]
    sd.potentiometers[:] = [512, 768]
    sd.ref_diode = 900
    sd.temp_sensor = 36.5
    sd.imu[:] = [0.01, 0.02, 0.03, 0.1, 0.2, 0.3]

    # Lock used to secure reading/writing from/to 'sd' (sensor data variable)
    lock = threading.Lock()

    # Start all sensor update threads
    threads = [
        threading.Thread(target=update_motor_encoders, args=(sd,lock), daemon=True),
        threading.Thread(target=update_home_switches, args=(sd,lock), daemon=True),
        threading.Thread(target=update_potentiometers, args=(sd,lock), daemon=True),
        threading.Thread(target=update_ref_diode, args=(sd,lock), daemon=True),
        threading.Thread(target=update_temperature, args=(sd,lock), daemon=True),
        threading.Thread(target=update_imu, args=(sd,lock), daemon=True),
    ]
    for t in threads:
        t.start()

    # Send updates every 100ms
    update_period = 100  # ms
    try:
        while True:
            with lock:
                msg = sensor_data_to_string(sd)
            print(msg)
            sm.send(msg)
            time.sleep(update_period / 1000)
    except KeyboardInterrupt:
        sm.stop()
        # Safe cleanup
        for f in ["a_to_b.txt", "b_to_a.txt"]:
            if os.path.exists(f):
                os.remove(f)

