from ctypes import Structure, c_uint16, c_bool, c_float

# Sensor Data structure
class SensorData(Structure):
    _fields_ = [
        ("motor_encoders", c_uint16 * 4),
        ("home_switches", c_bool * 4),
        ("potentiometers", c_uint16 * 2),
        ("ref_diode", c_uint16),
        ("temp_sensor", c_float),
        ("imu", c_float * 6)
    ]

    def __init__(self):
        super().__init__()
        self.system_log = ""

# Serialize SensorData to string
def sensor_data_to_string(sensor: SensorData) -> str:
    values = []
    values.extend(sensor.motor_encoders[:])
    values.extend(int(b) for b in sensor.home_switches[:])
    values.extend(sensor.potentiometers[:])
    values.append(sensor.ref_diode)
    values.append(f"{sensor.temp_sensor:.3f}")
    values.extend(f"{v:.3f}" for v in sensor.imu[:])
    values.append(f'"{sensor.system_log}"')
    return ",".join(str(v) for v in values)

# Deserialize string to SensorData
def string_to_sensor_data(msg: str) -> SensorData:
    parts = msg.split(",")
    sd = SensorData()
    sd.motor_encoders[:] = [int(parts[i]) for i in range(4)]
    sd.home_switches[:] = [bool(int(parts[i])) for i in range(4,8)]
    sd.potentiometers[:] = [int(parts[i]) for i in range(8,10)]
    sd.ref_diode = int(parts[10])
    sd.temp_sensor = float(parts[11])
    sd.imu[:] = [float(parts[i]) for i in range(12,18)]
    sd.system_log = parts[18].strip('"')
    return sd
