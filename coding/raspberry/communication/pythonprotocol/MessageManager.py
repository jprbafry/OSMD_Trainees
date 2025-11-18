import struct

MOTOR_ENCODER_MASK = (1 << 0)
HOME_SWITCH_MASK   = (1 << 1)
POTENTIOMETER_MASK = (1 << 2)
REF_DIODE_MASK     = (1 << 3)
TEMP_SENSOR_MASK   = (1 << 4)
IMU_MASK           = (1 << 5)

WAIT_FOR_START = 1
WAIT_FOR_MASK = 2
WAIT_FOR_LENGTH = 3
WAIT_FOR_PAYLOAD = 4

START_BYTE = 0xFF

class MessageManager:

    def __init__(self):
        self.data = {
            'motor_encoders': [0] * 4,    # uint16_t[4]
            'home_switches': [0] * 4,     # uint8_t[4]
            'potentiometers': [0] * 2,    # uint16_t[2]
            'ref_diode': 0,               # uint16_t
            'temp_sensor': 0.0,           # float
            'imu': [0.0] * 6              # float[6]
        }

        self.mask = 0
        self.length = 0
        self.readState = WAIT_FOR_START
        self.payload = bytearray(64)
        self.payload_index = 0

    def PackPayloadFromData(self):
        ptr = 0

        if self.mask & MOTOR_ENCODER_MASK:
            struct.pack_into('<4H', self.payload, ptr, *self.data['motor_encoders'])
            ptr += 4 * 2

        if self.mask & HOME_SWITCH_MASK:
            struct.pack_into('<4B', self.payload, ptr, *self.data['home_switches'])
            ptr += 4 * 1

        if self.mask & POTENTIOMETER_MASK:
            struct.pack_into('<2H', self.payload, ptr, *self.data['potentiometers'])
            ptr += 2 * 2

        if self.mask & REF_DIODE_MASK:
            struct.pack_into('<H', self.payload, ptr, self.data['ref_diode'])
            ptr += 2

        if self.mask & TEMP_SENSOR_MASK:
            struct.pack_into('<f', self.payload, ptr, self.data['temp_sensor'])
            ptr += 4

        if self.mask & IMU_MASK:
            struct.pack_into('<6f', self.payload, ptr, *self.data['imu'])
            ptr += 6 * 4

        self.length = ptr

    def LoadDataFromPayload(self):
        ptr = 0
        
        if self.mask & MOTOR_ENCODER_MASK:
            self.data['motor_encoders'] = list(struct.unpack_from('<4H', self.payload, ptr))
            ptr += 4 * 2

        if self.mask & HOME_SWITCH_MASK:
            self.data['home_switches'] = list(struct.unpack_from('<4B', self.payload, ptr))
            ptr += 4 * 1

        if self.mask & POTENTIOMETER_MASK:
            self.data['potentiometers'] = list(struct.unpack_from('<2H', self.payload, ptr))
            ptr += 2 * 2

        if self.mask & REF_DIODE_MASK:
            (self.data['ref_diode']) = struct.unpack_from('<H', self.payload, ptr)
            ptr += 2

        if self.mask & TEMP_SENSOR_MASK:
            (self.data['temp_sensor']) = struct.unpack_from('<f', self.payload, ptr)
            ptr += 4

        if self.mask & IMU_MASK:
            self.data['imu'] = list(struct.unpack_from('<6f', self.payload, ptr))
            ptr += 6 * 4

    def ReadMessage(self, b): 
        b = b[0]  

        if self.readState == WAIT_FOR_START:
            if b == START_BYTE:
                self.readState = WAIT_FOR_MASK

        elif self.readState == WAIT_FOR_MASK:
            self.mask = b
            self.readState = WAIT_FOR_LENGTH

        elif self.readState == WAIT_FOR_LENGTH:
            self.length = b
            self.payload_index = 0
            self.readState = WAIT_FOR_PAYLOAD

        elif self.readState == WAIT_FOR_PAYLOAD:
            self.payload[self.payload_index] = b
            self.payload_index += 1

            if self.payload_index >= self.length:
                self.LoadDataFromPayload()
                self.readState = WAIT_FOR_START

    def ReadMessageSimulation(self, line):
        if len(line) == 0:
            return

        if self.readState == WAIT_FOR_START:
            value = int(line[0])
            if value == START_BYTE:
                self.readState = WAIT_FOR_MASK

        elif self.readState == WAIT_FOR_MASK:
            value = int(line[0])
            self.mask = value
            self.readState = WAIT_FOR_LENGTH

        elif self.readState == WAIT_FOR_LENGTH:
            value = int(line[0])
            self.length = value
            self.payload_index = 0
            self.readState = WAIT_FOR_PAYLOAD

        elif self.readState == WAIT_FOR_PAYLOAD:
            for value in line:
                value = int(value)
                self.payload[self.payload_index] = value
                self.payload_index += 1

                if self.payload_index >= self.length:   # full packet received
                    try:
                        self.LoadDataFromPayload()
                    except Exception as e:
                        print(f"Error unpacking payload in simulation: {e}")
                    self.readState = WAIT_FOR_START
    
    # SETTERS
    def SetMotorEncoders(self, motor_encoder_data) -> str: 
        self.data['motor_encoders'] = list(motor_encoder_data)
        self.mask |= MOTOR_ENCODER_MASK

    def SetHomeSwitches(self, home_switch_data):
        self.data['home_switches'] = list(home_switch_data)
        self.mask |= HOME_SWITCH_MASK

    def SetPotentiometers(self, potentiometer_data):
        self.data['potentiometers'] = list(potentiometer_data)
        self.mask |= POTENTIOMETER_MASK

    def SetRefDiode(self, ref_diode_data):
        self.data['ref_diode'] = ref_diode_data
        self.mask |= REF_DIODE_MASK

    def SetTempSensor(self, temp_sensor_data):
        self.data['temp_sensor'] = temp_sensor_data
        self.mask |= TEMP_SENSOR_MASK

    def SetIMU(self, imu_data):
        self.data['imu'] = list(imu_data)
        self.mask |= IMU_MASK