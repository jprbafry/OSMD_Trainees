#include <Arduino.h>
#include <Thread.h>
#include <ThreadController.h>
#include <Wire.h>
#include <math.h>

//----------------------
// Configuration
//----------------------
#define BAUD_RATE 19200

//----------------------
// SensorData
//----------------------
typedef struct {
  uint16_t motor_encoders[4];
  bool home_switches[4];
  uint16_t potentiometers[2];
  uint16_t ref_diode;
  float temp_sensor;
  float imu[6];
} SensorData;

//----------------------
// Global Variables
//----------------------
SensorData sd;
float imu_phase[6];
float imu_freq[6];
int encoder_dir[4];
float start_time;

//----------------------
// Task Intervals (ms)
//----------------------
#define PER_ENCODERS   20
#define PER_HOME       40
#define PER_POTS       40
#define PER_REFDIODE   100
#define PER_TEMP       200
#define PER_IMU        20
#define PER_PRINT      20

//----------------------
// Thread Controller
//----------------------
ThreadController controller = ThreadController();
Thread tEncoders = Thread();
Thread tHome = Thread();
Thread tPots = Thread();
Thread tRefDiode = Thread();
Thread tTemp = Thread();
Thread tIMU = Thread();
Thread tPrint = Thread();

//----------------------
// Initialization
//----------------------
void init_sensor_data() {
  sd.motor_encoders[0] = 511;
  sd.motor_encoders[1] = 255;
  sd.motor_encoders[2] = 127;
  sd.motor_encoders[3] = 63;
  for (int i = 0; i < 4; i++) sd.home_switches[i] = false;
  sd.potentiometers[0] = 512;
  sd.potentiometers[1] = 768;
  sd.ref_diode = 900;
  sd.temp_sensor = 36.5;

  for (int i = 0; i < 6; i++) {
    sd.imu[i] = 0;
    imu_phase[i] = (float)(i * M_PI / 3.0);
    imu_freq[i] = 1.0 + ((float)random(0, 400) / 100.0); // 1–5 Hz range
  }

  for (int i = 0; i < 4; i++) encoder_dir[i] = 1;

  start_time = millis() / 1000.0;
}

//----------------------
// Utility function to emulate time
//----------------------
float get_time_seconds() {
  return millis() / 1000.0;
}

//----------------------
// Tasks
//----------------------
void TaskMotorEncoders() {
  for (int i = 0; i < 4; i++) {
    int lim = (i < 2) ? 511 : 255;
    sd.motor_encoders[i] += encoder_dir[i];
    if (sd.motor_encoders[i] >= lim) {
      sd.motor_encoders[i] = lim;
      encoder_dir[i] = -1;
    } else if (sd.motor_encoders[i] == 0) {
      encoder_dir[i] = 1;
    }
  }
}

void TaskHomeSwitches() {
  for (int i = 0; i < 4; i++) {
    sd.home_switches[i] = (sd.motor_encoders[i] < 5);
  }
}

void TaskPotentiometers() {
  sd.potentiometers[0] = sd.motor_encoders[2];
  sd.potentiometers[1] = sd.motor_encoders[3];
}

void TaskRefDiode() {
  int noise = random(-20, 21);
  sd.ref_diode = 650 + noise;
}

void TaskTemperature() {
  float t = get_time_seconds() - start_time;
  sd.temp_sensor = 16 + 8 * sin(2 * M_PI * t / 86400.0f);
}

void TaskIMU() {
  float t = get_time_seconds() - start_time;
  for (int i = 0; i < 6; i++) {
    sd.imu[i] = sin(imu_freq[i] * t + imu_phase[i]);
  }
}

void TaskPrint() {
  String msg = "";

  // motor_encoders[4]
  for (int i = 0; i < 4; i++) {
    msg += String(sd.motor_encoders[i]);
    msg += ",";
  }

  // home_switches[4]
  for (int i = 0; i < 4; i++) {
    msg += String((int)sd.home_switches[i]);
    msg += ",";
  }

  // potentiometers[2]
  for (int i = 0; i < 2; i++) {
    msg += String(sd.potentiometers[i]);
    msg += ",";
  }

  // ref_diode
  msg += String(sd.ref_diode);
  msg += ",";

  // temp_sensor
  msg += String(sd.temp_sensor, 3);
  msg += ",";

  // imu[6]
  for (int i = 0; i < 6; i++) {
    msg += String(sd.imu[i], 3);
    if (i < 5) msg += ",";
  }

  Serial.println(msg);
}

//----------------------
// Setup
//----------------------
void setup() {
  Serial.begin(BAUD_RATE);
  Wire.begin();
  randomSeed(analogRead(0));
  init_sensor_data();

  // Setup threads
  tEncoders.onRun(TaskMotorEncoders);
  tEncoders.setInterval(PER_ENCODERS);
  controller.add(&tEncoders);

  tHome.onRun(TaskHomeSwitches);
  tHome.setInterval(PER_HOME);
  controller.add(&tHome);

  tPots.onRun(TaskPotentiometers);
  tPots.setInterval(PER_POTS);
  controller.add(&tPots);

  tRefDiode.onRun(TaskRefDiode);
  tRefDiode.setInterval(PER_REFDIODE);
  controller.add(&tRefDiode);

  tTemp.onRun(TaskTemperature);
  tTemp.setInterval(PER_TEMP);
  controller.add(&tTemp);

  tIMU.onRun(TaskIMU);
  tIMU.setInterval(PER_IMU);
  controller.add(&tIMU);

  tPrint.onRun(TaskPrint);
  tPrint.setInterval(PER_PRINT);
  controller.add(&tPrint);
}

void loop() {
  controller.run(); // ArduinoThread scheduler
}
