#include <Arduino.h>
#include <Wire.h>
#include <Arduino_FreeRTOS.h>


// -------------------------
// Configuration
// -------------------------
#define BAUD_RATE 115200

// -------------------------
// Sensor Data Structure
// -------------------------
struct SensorData {
  int pot_light;
  int pot_detector;
  int ref_diode;
  bool home_detector_azi;
  bool home_light_azi;
  bool home_light_pol;
  bool home_detector_pol;
  float accelX, accelY, accelZ;
  float gyroX, gyroY, gyroZ;
  float tempIMU;
};

// Global shared data
volatile SensorData sensors;

// -------------------------
// Pin Definitions
// -------------------------
const int PIN_POT_LIGHT = A0;
const int PIN_POT_DETECTOR = A1;
const int PIN_REFDIODE = A2;

const int PIN_HOME_SWT_DETECTOR_AZI = 46;
const int PIN_HOME_SWT_LIGHT_AZI = 47;
const int PIN_HOME_SWT_LIGHT_POL = 48;
const int PIN_HOME_SWT_DETECTOR_POL = 49;

const int PIN_LED_1 = 26;
const int PIN_LED_2 = 27;
const int PIN_LED_3 = 28;
const int PIN_LED_4 = 29;


// -------------------------
// Task Intervals (ms)
// -------------------------
#define PER_POT_AZI      100
#define PER_REFDIODE     100
#define PER_HOME_POLAR   100
#define PER_HOME_AZI     100
#define PER_LED          50
#define PER_PRINTER      1000
#define PER_IMU          100

// -------------------------
// Task Functions
// -------------------------
void TaskPot(void *pvParameters) {
  for (;;) {
    sensors.pot_light = analogRead(PIN_POT_LIGHT);
    sensors.pot_detector = analogRead(PIN_POT_DETECTOR);
    vTaskDelay(PER_POT_AZI / portTICK_PERIOD_MS);
  }
}

void TaskRefDiode(void *pvParameters) {
  for (;;) {
    sensors.ref_diode = analogRead(PIN_REFDIODE);
    vTaskDelay(PER_REFDIODE / portTICK_PERIOD_MS);
  }
}

void TaskPolarSwitches(void *pvParameters) {
  for (;;) {
    sensors.home_light_pol = !digitalRead(PIN_HOME_SWT_LIGHT_POL);
    sensors.home_detector_pol = !digitalRead(PIN_HOME_SWT_DETECTOR_POL);
    vTaskDelay(PER_HOME_POLAR / portTICK_PERIOD_MS);
  }
}

void TaskAzimuthalSwitches(void *pvParameters) {
  for (;;) {
    sensors.home_light_azi = !digitalRead(PIN_HOME_SWT_LIGHT_AZI);
    sensors.home_detector_azi = !digitalRead(PIN_HOME_SWT_DETECTOR_AZI);
    vTaskDelay(PER_HOME_AZI / portTICK_PERIOD_MS);
  }
}

void TaskLED(void *pvParameters) {
  for (;;) {
    digitalWrite(PIN_LED_1, sensors.home_detector_azi ? HIGH : LOW);
    digitalWrite(PIN_LED_2, sensors.home_light_azi ? HIGH : LOW);
    digitalWrite(PIN_LED_3, sensors.home_light_pol ? HIGH : LOW);
    digitalWrite(PIN_LED_4, sensors.home_detector_pol ? HIGH : LOW);
    vTaskDelay(PER_LED / portTICK_PERIOD_MS);
  }
}

/* void TaskIMU(void *pvParameters) {
  for (;;) {
    sensors.accelX = imu.getAccelerationX();
    sensors.accelY = imu.getAccelerationY();
    sensors.accelZ = imu.getAccelerationZ();
    sensors.gyroX = imu.getRotationX();
    sensors.gyroY = imu.getRotationY();
    sensors.gyroZ = imu.getRotationZ();
    sensors.tempIMU = imu.getTemperature();
    vTaskDelay(PER_IMU / portTICK_PERIOD_MS);
  }
} */

void TaskPrint(void *pvParameters) {
  for (;;) {
    Serial.print(F("Signals ... "));
    Serial.print(F(" Light_pot: ")); Serial.print(sensors.pot_light);
    Serial.print(F(" Detector_pot: ")); Serial.print(sensors.pot_detector);
    Serial.print(F(" Ref_diode: ")); Serial.print(sensors.ref_diode);
    Serial.println();

    Serial.print(F("Homing ... "));
    Serial.print(F(" Light_pol: ")); Serial.print(sensors.home_light_pol);
    Serial.print(F(" Light_azi: ")); Serial.print(sensors.home_light_azi);
    Serial.print(F(" Detector_pol: ")); Serial.print(sensors.home_detector_pol);
    Serial.print(F(" Detector_azi: ")); Serial.print(sensors.home_detector_azi);
    Serial.println();

/*     Serial.print(F("IMU ... "));
    Serial.print(F(" Ax: ")); Serial.print(sensors.accelX);
    Serial.print(F(" Ay: ")); Serial.print(sensors.accelY);
    Serial.print(F(" Az: ")); Serial.print(sensors.accelZ);
    Serial.print(F(" Gx: ")); Serial.print(sensors.gyroX);
    Serial.print(F(" Gy: ")); Serial.print(sensors.gyroY);
    Serial.print(F(" Gz: ")); Serial.println(sensors.gyroZ);
    Serial.print(F(" T: ")); Serial.println(sensors.tempIMU);
    Serial.println(); */

    vTaskDelay(PER_PRINTER / portTICK_PERIOD_MS);
  }
}

// -------------------------
// Setup
// -------------------------
void setup() {
  Serial.begin(BAUD_RATE);
  Wire.begin();

  pinMode(PIN_HOME_SWT_LIGHT_POL, INPUT_PULLUP);
  pinMode(PIN_HOME_SWT_LIGHT_AZI, INPUT_PULLUP);
  pinMode(PIN_HOME_SWT_DETECTOR_POL, INPUT_PULLUP);
  pinMode(PIN_HOME_SWT_DETECTOR_AZI, INPUT_PULLUP);
  pinMode(PIN_LED_1, OUTPUT);
  pinMode(PIN_LED_2, OUTPUT);

  // --- Create Tasks ---
  xTaskCreate(TaskPot, "Pots", 128, NULL, 1, NULL);
  xTaskCreate(TaskRefDiode, "Ref", 128, NULL, 1, NULL);
  xTaskCreate(TaskPolarSwitches, "Switches", 128, NULL, 1, NULL);
  xTaskCreate(TaskAzimuthalSwitches, "Azi", 128, NULL, 1, NULL);
  xTaskCreate(TaskLED, "LED", 128, NULL, 1, NULL);
  //xTaskCreate(TaskIMU, "IMU", 256, NULL, 1, NULL);
  xTaskCreate(TaskPrint, "Print", 256, NULL, 1, NULL);

}

void loop() {
  // Tasks are running under FreeRTOS
}
