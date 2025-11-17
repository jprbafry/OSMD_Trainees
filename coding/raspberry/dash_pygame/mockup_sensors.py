import threading
import time
import math
import random
import os
import argparse

from communication.mux_tx_rx import SerialManager
from communication.pythonprotocol import MessageManager

from communication.ComsModule import MessageManager as ComsMessageManager

# Function to update motor encoders data
def update_motor_encoders(mm: MessageManager, lock: threading.Lock, step=1, period_ms=20):
    direction = [1]*4
    motor_encoders = [1]*4
    while True:
        with lock:
            for i in range(4):
                if i < 2:
                    lim = 511
                else:
                    lim = 255
                motor_encoders[i] += direction[i]*step
                if motor_encoders[i] >= lim:
                    motor_encoders[i] = lim
                    direction[i] = -1
                elif motor_encoders[i] <= 0:
                    motor_encoders[i] = 0
                    direction[i] = 1
            # C++ VERSION
            # mm.setMotorEncoders(motor_encoders)

            # PYTHON VERSION
            mm.SetMotorEncoders(motor_encoders)
        time.sleep(period_ms / 1000)

# Function to update Homing sensors data
def update_home_switches(mm: MessageManager, lock: threading.Lock, period_ms=40):
    home_switches = [1]*4
    while True:
        with lock:
            # C++ VERSION
            '''
            sensors = mm.getSensors()
            for i in range(4):
                home_switches[i] = (sensors.motor_encoders[i] < 5)
            mm.setHomeSwitches(home_switches)
            '''
            #PYTHON VERSION
            sensors = mm.data
            for i in range(4):
                home_switches[i] = (sensors['motor_encoders'][i] < 5)
            mm.SetHomeSwitches(home_switches)

        time.sleep(period_ms / 1000)

# Function to update Potentiometers data
def update_potentiometers(mm: MessageManager, lock: threading.Lock, period_ms=40):
    while True:
        with lock:
            # C++ VERSION
            '''
            sensors = mm.getSensors()
            mm.setPotentiometers([sensors.motor_encoders[2], sensors.motor_encoders[3]])
            '''
            #PYTHON VERSION
            sensors = mm.data
            mm.SetPotentiometers([sensors['motor_encoders'][2], sensors['motor_encoders'][3]])
        time.sleep(period_ms / 1000)

# Function to update Reference Diode data
def update_ref_diode(mm: MessageManager, lock: threading.Lock, period_ms=100):
    while True:
        with lock:
            #C++ VERSION
            #mm.setRefDiode(650 + random.randint(-20,20))

            #PYTHON VERSION
            mm.SetRefDiode(650 + random.randint(-20,20))
        time.sleep(period_ms / 1000)

# Function to update Temperature data
def update_temperature(mm: MessageManager, lock: threading.Lock, period_ms=200):
    start_time = time.time()
    while True:
        with lock:
            t = time.time() - start_time
            #C++ VERSION
            #mm.setTempSensor(16 + 8 * math.sin(2*math.pi * t / (24*60*60)))

            #PYTHON VERSION
            mm.SetTempSensor(16 + 8 * math.sin(2*math.pi * t / (24*60*60)))
        time.sleep(period_ms / 1000)

# Function to update IMU data
def update_imu(mm: MessageManager, lock: threading.Lock, period_ms=20):
    start_time = time.time()
    phases = [0, math.pi/3, 2*math.pi/3, math.pi, 4*math.pi/3, 5*math.pi/3]
    freqs = [random.uniform(1,5) for _ in range(6)]
    amplitude = 1.0
    imu = [1]*6
    while True:
        with lock:  
            t = time.time() - start_time
            for i in range(6):
                imu[i] = amplitude * math.sin(freqs[i]*t + phases[i])
            # C++ VERSION
            #mm.setImus(imu)

            # PYTHON VERSION
            mm.SetIMU(imu)
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


    # Lock used to secure reading/writing from/to 'sd' (sensor data variable)
    lock = threading.Lock()

    # Start all sensor update threads
    # C++ VERSION
    '''
    threads = [
        threading.Thread(target=update_motor_encoders, args=(sm.comsMsgManagerSend,lock), daemon=True),
        threading.Thread(target=update_home_switches, args=(sm.comsMsgManagerSend,lock), daemon=True),
        threading.Thread(target=update_potentiometers, args=(sm.comsMsgManagerSend,lock), daemon=True),
        threading.Thread(target=update_ref_diode, args=(sm.comsMsgManagerSend,lock), daemon=True),
        threading.Thread(target=update_temperature, args=(sm.comsMsgManagerSend,lock), daemon=True),
        threading.Thread(target=update_imu, args=(sm.comsMsgManagerSend,lock), daemon=True),
    ]
    '''
    # PYTHON VERSION
    threads = [
        threading.Thread(target=update_motor_encoders, args=(sm.msgManagerSend,lock), daemon=True),
        threading.Thread(target=update_home_switches, args=(sm.msgManagerSend,lock), daemon=True),
        threading.Thread(target=update_potentiometers, args=(sm.msgManagerSend,lock), daemon=True),
        threading.Thread(target=update_ref_diode, args=(sm.msgManagerSend,lock), daemon=True),
        threading.Thread(target=update_temperature, args=(sm.msgManagerSend,lock), daemon=True),
        threading.Thread(target=update_imu, args=(sm.msgManagerSend,lock), daemon=True),
    ]

    for t in threads:
        t.start()

    # Send updates every 100ms
    update_period = 40  # ms
    try:
        while True:
            with lock:
                """
                # C++ VERSION
                sm.comsMsgManagerSend.packPayload()
                payload = sm.comsMsgManagerSend.getPayload()

                print("Sending message with mask:", sm.comsMsgManagerSend.mask)
                print("Sending message with length:", sm.comsMsgManagerSend.length)
                print("Sending message with msg:", payload[:sm.comsMsgManagerSend.length])

                sm.send(0xFF) #Send start byte
                sm.send(sm.comsMsgManagerSend.mask) #Send mask byte
                sm.send(sm.comsMsgManagerSend.length) #Send length byte
                sm.send(payload[:sm.comsMsgManagerSend.length])
                
                sm.comsMsgManagerSend.mask = 0
                """

                #PYTHON VERSION
                sm.msgManagerSend.PackPayloadFromData()
                msg = sm.msgManagerSend.payload[:sm.msgManagerSend.length]
                
                sm.send(0xFF) #Send start byte
                sm.send(sm.msgManagerSend.mask) #Send mask byte
                sm.send(sm.msgManagerSend.length) #Send length byte
                sm.send(msg)

                sm.msgManagerSend.mask = 0


            time.sleep(update_period / 1000)
    except KeyboardInterrupt:
        sm.stop()
        # Safe cleanup
        for f in ["a_to_b.txt", "b_to_a.txt"]:
            if os.path.exists(f):
                os.remove(f)

"""
How to implement our custom comms protocol:
    1. Include custom comms files in folder and allow for python code to call it using Pybind11
    2. Create instance of class to save sensor data
    3. Adjust update_*sensor* functions called in threads to update sensor data and mask in protocol
    4. Replace sensor_data_to_string(sd) with our own function
    5. Call protocol functions for sending data over serial <--


    QUESTIONS: 

    Is this repo intended to run in a virtual environment? If so, can we add pybind11 to it? else, can we add it as submodule in github?

    Should we simulate it from our end in Malmö, i.e. hardware agnostic, keeping the a-to-b.txt and b-to-a.txt solution for testing purposes? 
    Or should we do it with the actual Arduino and Raspberry Pi?
 
    ANSWERS:

    We do create our own virtual envs, but we have not made it formal (we have not created the requirements.txt).

    I think having it agnostic is good, since we can test without hardware, just please make sure it runs with the arduino aswell :) 

"""