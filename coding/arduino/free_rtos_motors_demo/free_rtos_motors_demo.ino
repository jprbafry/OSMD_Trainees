#include <Arduino.h>
#include <Arduino_FreeRTOS.h>

// === Pin Definitions ===
#define DET_AZ_STEP 34
#define DET_AZ_DIR 35
#define DET_RAD_STEP 32
#define DET_RAD_DIR 33
#define LIGHT_AZ_STEP 36
#define LIGHT_AZ_DIR 37
#define LIGHT_RAD_STEP 30
#define LIGHT_RAD_DIR 31

// === Constants ===
const float DET_AZ_STEPS_PER_DEG = 4.0;
const float DET_RAD_STEPS_PER_DEG = 18.0;
const float LIGHT_AZ_STEPS_PER_DEG = 24.0;
const float LIGHT_RAD_STEPS_PER_DEG = 18.0;

const unsigned int NUM_MOTORS = 4;
const unsigned int STEP_DELAY_US = 1000;

// === Enum for Axis Selection ===
enum MotorAxis {
  DETECTOR_AZ,
  DETECTOR_RAD,
  LIGHT_AZ,
  LIGHT_RAD
};

// === Motor struct ===
struct Motor {
  const char *name;
  int step_pin;
  int dir_pin;
  volatile uint8_t *step_port;
  uint8_t step_mask;
  volatile uint8_t *dir_port;
  uint8_t dir_mask;
  float steps_per_deg;
  long current_steps;
};

Motor motors[NUM_MOTORS];

// === Task periods (ms) ===
#define MOTION_PERIOD 2
#define RECEPTION_PERIOD 5
#define TRANSMISSION_PERIOD 40

// === Shared variables ===
float des_light_azi = 180.0, des_light_pol = 90.0;
float des_detector_azi = 180.0, des_detector_pol = 90.0;
float cur_light_azi = 180.0, cur_light_pol = 90.0;
float cur_detector_azi = 180.0, cur_detector_pol = 90.0;
String inputBuffer = "";

// === Function prototypes ===
void processInput(String msg);
Motor* get_motor(MotorAxis axis);
void stepMotorOnce(MotorAxis axis);

// === FreeRTOS task prototypes ===
void TaskReceive(void *pvParameters);
void TaskMoveM1(void *pvParameters);
void TaskMoveM2(void *pvParameters);
void TaskMoveM3(void *pvParameters);
void TaskMoveM4(void *pvParameters);
void TaskSend(void *pvParameters);

//------------------------------------------------------------------------
// SETUP
//------------------------------------------------------------------------
void setup() {
  Serial.begin(19200);
  while (!Serial) {;}

  // Map pins to ports & masks for direct port manipulation (Mega example)
  motors[DETECTOR_AZ]  = {"DET_AZ",  DET_AZ_STEP,  DET_AZ_DIR, &PORTC, _BV(6), &PORTC, _BV(7), DET_AZ_STEPS_PER_DEG, long(cur_detector_azi * DET_AZ_STEPS_PER_DEG)};
  motors[DETECTOR_RAD] = {"DET_RAD", DET_RAD_STEP, DET_RAD_DIR, &PORTC, _BV(4), &PORTC, _BV(5), DET_RAD_STEPS_PER_DEG, long(cur_detector_pol * DET_RAD_STEPS_PER_DEG)};
  motors[LIGHT_AZ]     = {"LIGHT_AZ",LIGHT_AZ_STEP, LIGHT_AZ_DIR, &PORTC, _BV(2), &PORTC, _BV(3), LIGHT_AZ_STEPS_PER_DEG, long(cur_light_azi * LIGHT_AZ_STEPS_PER_DEG)};
  motors[LIGHT_RAD]    = {"LIGHT_RAD",LIGHT_RAD_STEP, LIGHT_RAD_DIR, &PORTC, _BV(0), &PORTC, _BV(1), LIGHT_RAD_STEPS_PER_DEG, long(cur_light_pol * LIGHT_RAD_STEPS_PER_DEG)};

  for (int i = 0; i < NUM_MOTORS; ++i) {
    pinMode(motors[i].step_pin, OUTPUT);
    pinMode(motors[i].dir_pin, OUTPUT);
  }

  Serial.println(F("Motor controller (FreeRTOS + direct port) ready."));

  // Create FreeRTOS tasks
  xTaskCreate(TaskReceive, "Receive", 256, NULL, 2, NULL);
  xTaskCreate(TaskMoveM1, "MoveM1", 512, NULL, 1, NULL);
  xTaskCreate(TaskMoveM2, "MoveM2", 512, NULL, 1, NULL);
  xTaskCreate(TaskMoveM3, "MoveM3", 512, NULL, 1, NULL);
  xTaskCreate(TaskMoveM4, "MoveM4", 512, NULL, 1, NULL);
  xTaskCreate(TaskSend, "Send", 256, NULL, 1, NULL);
}

void loop() {}

//------------------------------------------------------------------------
// CORE FUNCTIONS
//------------------------------------------------------------------------
Motor* get_motor(MotorAxis axis) {
  return &motors[(int)axis];
}

void stepMotorOnce(MotorAxis axis) {
  Motor* m = get_motor(axis);
  long target_steps = lround((axis == LIGHT_RAD ? des_light_pol :
                              axis == DETECTOR_RAD ? des_detector_pol :
                              axis == DETECTOR_AZ ? des_detector_azi :
                              des_light_azi) * m->steps_per_deg);
  long step_diff = target_steps - m->current_steps;
  if (step_diff == 0) return;

  bool direction = (step_diff >= 0);

  // Set direction
  if (direction)
    *(m->dir_port) |= m->dir_mask;
  else
    *(m->dir_port) &= ~(m->dir_mask);

  // Short delay for DIR settling
  delayMicroseconds(10);

  // Pulse step pin
  *(m->step_port) |= m->step_mask;
  delayMicroseconds(200);
  *(m->step_port) &= ~(m->step_mask);
  delayMicroseconds(200);

  m->current_steps += (direction ? 1 : -1);
}

void processInput(String msg) {
  Serial.print(F("Arduino Received: "));
  Serial.println(msg);

  float vals[4];
  int lastIndex = 0;
  int commaIndex = 0;

  for (int i = 0; i < 4; i++) {
    commaIndex = msg.indexOf(',', lastIndex);
    String token;

    if (commaIndex == -1 && i < 3) return;  // malformed
    if (commaIndex == -1)
      token = msg.substring(lastIndex);
    else
      token = msg.substring(lastIndex, commaIndex);

    vals[i] = token.toFloat();
    lastIndex = commaIndex + 1;
  }

  des_light_azi = vals[0];
  des_light_pol = vals[1];
  des_detector_azi = vals[2];
  des_detector_pol = vals[3];
}

//------------------------------------------------------------------------
// TASKS
//------------------------------------------------------------------------

void TaskReceive(void *pvParameters) {
  (void) pvParameters;
  for (;;) {
    while (Serial.available()) {
      char c = Serial.read();
      if (c == '\n' || c == '\r') {
        if (inputBuffer.length() > 0) {
          processInput(inputBuffer);
          inputBuffer = "";
        }
      } else {
        inputBuffer += c;
      }
    }
    vTaskDelay(RECEPTION_PERIOD / portTICK_PERIOD_MS);
  }
}

void TaskMoveM1(void *pvParameters) { for (;;) { stepMotorOnce(LIGHT_RAD); vTaskDelay(MOTION_PERIOD / portTICK_PERIOD_MS); } }
void TaskMoveM2(void *pvParameters) { for (;;) { stepMotorOnce(DETECTOR_RAD); vTaskDelay(MOTION_PERIOD / portTICK_PERIOD_MS); } }
void TaskMoveM3(void *pvParameters) { for (;;) { stepMotorOnce(DETECTOR_AZ); vTaskDelay(MOTION_PERIOD / portTICK_PERIOD_MS); } }
void TaskMoveM4(void *pvParameters) { for (;;) { stepMotorOnce(LIGHT_AZ); vTaskDelay(MOTION_PERIOD / portTICK_PERIOD_MS); } }

void TaskSend(void *pvParameters) {
  (void) pvParameters;
  for (;;) {
    Serial.print(des_light_azi, 1); Serial.print(',');
    Serial.print(des_light_pol, 1); Serial.print(',');
    Serial.print(des_detector_azi, 1); Serial.print(',');
    Serial.println(des_detector_pol, 1);
    vTaskDelay(TRANSMISSION_PERIOD / portTICK_PERIOD_MS);
  }
}
