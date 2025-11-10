import threading
import os
import time
import logging
import numpy as np
from enum import IntEnum


from ComsModule import MessageManager


class defines(IntEnum):
    START_BYTE = 0xAA
    END_BYTE = 0xBB
    WAIT_FOR_START = 0XFE
    WAIT_FOR_PAYLOAD = 0XFF

try:
    import serial
except ImportError:
    serial = None


# Logging Setup
logger = logging.getLogger("SerialManager")
logger.setLevel(logging.DEBUG) # log everything
ch = logging.StreamHandler() # print to console
logger.addHandler(ch) # attach handler


# Simulated serial port using text files for inter-process comms
class FileBackedFakeSerial:

    def __init__(self, name):
        self.name = name.upper()
        base = os.path.dirname(__file__)
        if self.name == 'A':
            self.write_file = os.path.join(base, 'a_to_b.txt')
            self.read_file  = os.path.join(base, 'b_to_a.txt')
        elif self.name == 'B':
            self.write_file = os.path.join(base, 'b_to_a.txt')
            self.read_file  = os.path.join(base, 'a_to_b.txt')
        else:
            raise ValueError("Name must be 'A' or 'B'")

        # ensure files exist
        for f in [self.write_file, self.read_file]:
            open(f, 'a').close()

    def write(self, data: bytes):
        #print(f"Self name in write: {self.name}")
        #print(f"Writing to file: {self.write_file.split("/")[-1]}")
        with open(self.write_file, 'a', encoding='utf-8') as f:
            #f.write(data.decode("ascii"))
            print(f"Type: {type(data)}")

            if(type(data) == int):
                f.write(str(data))
            elif(type(data) == np.ndarray):
                for d in data:
                    if d and (d != "[" and d != "]"):
                        f.write(str(d) + " ")
            f.write("\n")

    def readline(self) -> bytes:
        line = ''
        with open(self.read_file, 'r+', encoding='utf-8') as f:
            f.seek(0)
            #print(f"Self name in read: {self.name}")
            #print(f"Reading from file: {self.read_file.split("/")[-1]}")
            #print(f"File content before reading: {str(content)}")
            lines = f.readlines()
            #print(f"Lines is: {lines}")
            if lines:
                line = lines[0]
                f.seek(0)
                f.writelines(lines[1:])
                f.truncate()
                print(f"Line is: {line}")
        return line.encode('ascii')

    def flush(self):
        pass

    def close(self):
        pass

# Class to handle Tx/Rx data over real or simulated serial
class SerialManager:

    def __init__(self, port="/dev/ttyACM0", baud=38400, simulate=True, name=None, debug=False):
        self.running = threading.Event()
        self.send_queue = []
        self.lock = threading.Lock()
        self.on_receive = None
        self.simulate = simulate
        self.msgmanager = MessageManager()
        self.readState = defines.WAIT_FOR_START

        if debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        if simulate or serial is None:
            if not name:
                raise ValueError("Need name='A' or 'B' when simulate=True")
            logger.info(f"Using simulated serial as {name}")
            self.ser = FileBackedFakeSerial(name)
        else:
            try:
                logger.info(f"Opening real serial port {port} @ {baud}")
                #Initialize our msgManager
                self.ser = serial.Serial(
                    port=port,
                    baudrate=baud,
                    timeout=1
                )
                logger.info("Serial port opened successfully.")
                time.sleep(2)  # wait for Arduino reset

            except Exception as e:
                logger.error(f"Could not open {port}: {e}")
                logger.warning("Falling back to simulation mode.")
                self.ser = FileBackedFakeSerial(name or 'A')
                self.simulate = True

        self.tx_thread = threading.Thread(target=self.tx_loop, daemon=True)
        self.rx_thread = threading.Thread(target=self.rx_loop, daemon=True)

    # Transmission Thread (function)
    def tx_loop(self):
        while self.running.is_set():
            with self.lock:
                if self.send_queue:
                    msg = self.send_queue.pop(0)
                    try:

                        # Tror vi kan skicka hela payloaden på en gång?
                        '''
                        for byte in self.msgmanager.getPayload():
                            if byte:
                                self.ser.write(str(byte))
                                print(f"Wrote {byte} to serial")
                                logger.debug(f"TX debug: {str(byte)}")
                        '''

                        self.ser.write(msg)

                        #print(f"Sent: {msg}")

                    except Exception as e:
                        logger.error(f"TX error: {e}")
            time.sleep(0.05)
        logger.debug("TX thread stopped")

    # Reception Thread (function)
    def rx_loop(self):
        while self.running.is_set():
            try:
                """
                line = self.ser.readline().decode('ascii', errors='ignore')
                if line:
                    if self.on_receive:
                        self.on_receive(line)
                        logger.debug(f"RX: {line}")
                    else:
                        logger.debug(f"RX: {line}")
                        """
                self.read_message_state_machine()
            except Exception as e:
                logger.error(f"RX error: {e}")
            time.sleep(0.005)
        logger.debug("RX thread stopped")


    def read_message_state_machine(self):
        byte = self.ser.readline().decode('ascii', errors='ignore').split()
        for b in byte:
            #print(f"Byte: {b}")
            #print(f"START_BYTE: {defines.START_BYTE}")
            #print(f"END_BYTE: {defines.END_BYTE}")
            #print(f"WAIT_FOR_START: {defines.WAIT_FOR_START}")
            #print(f"WAIT_FOR_PAYLOAD: {defines.WAIT_FOR_PAYLOAD}")

            self.on_receive(self.msgmanager)
            
            if(self.readState == defines.WAIT_FOR_START):
                print("In WAIT_FOR_START")
                if (int(b) == defines.START_BYTE):
                    print("Found START_BYTE")
                    self.readState = defines.WAIT_FOR_PAYLOAD

            elif(self.readState == defines.WAIT_FOR_PAYLOAD):
                try:
                    self.msgmanager.fillPayload(int(b))
                except Exception as e:
                    print(f"Error in fillPayload(): {e}")
                #print("IN WAIT_FOR_PAYLOAD")
                if (int(b) == defines.END_BYTE):
                    print("Found END_BYTE")
                    self.msgmanager.loadData()
                    print(f"Temp sensor: {self.msgmanager.getSensors().temp_sensor}")
                    self.readState = defines.WAIT_FOR_START
        
        
    
    
    def start(self):
        self.running.set()
        self.tx_thread.start()
        self.rx_thread.start()
        logger.info("SerialManager started")

    def stop(self):
        self.running.clear()
        time.sleep(0.2)
        try:
            self.ser.close()
        except Exception:
            pass
        logger.info("SerialManager stopped")

    
    def send(self, msg):
        with self.lock:
            self.send_queue.append(msg)
