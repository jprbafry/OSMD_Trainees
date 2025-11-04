#include <Arduino.h>
#include <Arduino_FreeRTOS.h>
#include <Wire.h>
#include <math.h>

// -------------------------
// Configuration
// -------------------------
#define BAUD_RATE 19200

// -------------------------
// SensorData
// -------------------------
typedef struct {
  uint16_t motor_encoders[4];
  bool home_switches[4];
  uint16_t potentiometers[2];
  uint16_t ref_diode;
  float temp_sensor;
  float imu[6];
} SensorData;

// -------------------------
// Global Variables
// -------------------------
volatile SensorData sd;
volatile float imu_phase[6];
volatile float imu_freq[6];
volatile int encoder_dir[4];

// -------------------------
// Task Intervals (ms)
// -------------------------
#define PER_ENCODERS   20
#define PER_HOME       40
#define PER_POTS       40
#define PER_REFDIODE   100
#define PER_TEMP       200
#define PER_IMU        20
#define PER_PRINT      20

// -------------------------
// Initialization
// -------------------------
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
}

// -------------------------
// Utility function to emulate time
// -------------------------
float get_time_seconds() {
  return millis() / 1000.0;
}

// -------------------------
// Tasks
// -------------------------
void TaskMotorEncoders(void *pvParameters) {
  for (;;) {
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
    vTaskDelay(PER_ENCODERS / portTICK_PERIOD_MS);
  }
}

void TaskHomeSwitches(void *pvParameters) {
  for (;;) {
    for (int i = 0; i < 4; i++) {
      sd.home_switches[i] = (sd.motor_encoders[i] < 5);
    }
    vTaskDelay(PER_HOME / portTICK_PERIOD_MS);
  }
}

void TaskPotentiometers(void *pvParameters) {
  for (;;) {
    sd.potentiometers[0] = sd.motor_encoders[2];
    sd.potentiometers[1] = sd.motor_encoders[3];
    vTaskDelay(PER_POTS / portTICK_PERIOD_MS);
  }
}

void TaskRefDiode(void *pvParameters) {
  for (;;) {
    int noise = random(-20, 21);
    sd.ref_diode = 650 + noise;
    vTaskDelay(PER_REFDIODE / portTICK_PERIOD_MS);
  }
}

void TaskTemperature(void *pvParameters) {
  float start = get_time_seconds();
  for (;;) {
    float t = get_time_seconds() - start;
    sd.temp_sensor = 16 + 8 * sin(2 * M_PI * t / 86400.0f);

    vTaskDelay(PER_TEMP / portTICK_PERIOD_MS);
  }
}

void TaskIMU(void *pvParameters) {
  float start = get_time_seconds();
  for (;;) {
    float t = get_time_seconds() - start;
    for (int i = 0; i < 6; i++) {
      sd.imu[i] = sin(imu_freq[i] * t + imu_phase[i]);
    }
    vTaskDelay(PER_IMU / portTICK_PERIOD_MS);
  }
}

void TaskPrint(void *pvParameters) {
  for (;;) {
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
    vTaskDelay(PER_PRINT / portTICK_PERIOD_MS);
  }
}

// -------------------------
// Setup
// -------------------------
void setup() {
  Serial.begin(BAUD_RATE);
  Wire.begin();
  randomSeed(analogRead(0));
  init_sensor_data();

  xTaskCreate(TaskMotorEncoders, "Encoders", 256, NULL, 1, NULL);
  xTaskCreate(TaskHomeSwitches, "Home", 128, NULL, 1, NULL);
  xTaskCreate(TaskPotentiometers, "Pots", 128, NULL, 1, NULL);
  xTaskCreate(TaskRefDiode, "Ref", 128, NULL, 1, NULL);
  xTaskCreate(TaskTemperature, "Temp", 256, NULL, 1, NULL);
  xTaskCreate(TaskIMU, "IMU", 256, NULL, 1, NULL);
  xTaskCreate(TaskPrint, "Print", 512, NULL, 1, NULL);
}

void loop() {
  // Nothing here, FreeRTOS runs all tasks
}
