from dataclasses import dataclass, field

@dataclass
class SensorDataPy:
    """data class for Python (Raspberry) side"""
    motor_encoders: list[int] = field(default_factory=lambda: [0] * 4)
    home_switches: list[bool] = field(default_factory=lambda: [False] * 4)
    potentiometers: list[int] = field(default_factory=lambda: [0] * 2)
    ref_diode: int = 0
    temp_sensor: float = 0.0
    imu: list[float] = field(default_factory=lambda: [0.0] * 6)