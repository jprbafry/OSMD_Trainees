#include <Arduino.h>
#include <Thread.h>
#include <ThreadController.h>

/* 

This code creates three cooperative (as oppposed to preemptive) threads
    - tempThread: produces temperature data
*/


// --------------------------------------
// Data structure
// --------------------------------------
struct SensorData {
  float temperature;
};

SensorData sensors;

// --------------------------------------
// Threads
// --------------------------------------
ThreadController controller;
Thread tempThread;
Thread printThread;

// --------------------------------------
// Timing
// --------------------------------------
unsigned long startMillis;

// --------------------------------------
// Helper: pseudo-random float in [-range, +range]
// --------------------------------------
float randNoise(float range) {
  return ((float)random(-1000, 1000) / 1000.0f) * range;
}

// --------------------------------------
// Thread functions
// --------------------------------------

// Temperature: sinusoidal over 1 day (24h), amplitude 8°C, offset 16°C, ±0.1 noise
void updateTemperature() {
  float t_sec = (millis() - startMillis) / 1000.0f;
  const float day_period = 24.0f * 60.0f * 60.0f; // seconds in one day
  const float omega = 2.0f * PI / day_period;     // angular frequency
  float temp = 16.0f + 8.0f * sin(omega * t_sec); // offset + amplitude*sin()
  temp += randNoise(0.1f);
  sensors.temperature = temp;
}



// Print thread
void printSensors() {
  Serial.print("Temp: ");
  Serial.print(sensors.temperature, 2);
  Serial.print("°C\n");
}

// --------------------------------------
// Setup
// --------------------------------------
void setup() {
  Serial.begin(115200);
  delay(500);
  randomSeed(analogRead(A0)); // seed noise
  startMillis = millis();

  // Configure threads
  tempThread.onRun(updateTemperature);
  tempThread.setInterval(5000);   // every 5 seconds

  printThread.onRun(printSensors);
  printThread.setInterval(5000);   // every 5 seconds

  // Add to controller
  controller.add(&tempThread);
  //controller.add(&accelThread);
  controller.add(&printThread);
}

// --------------------------------------
// Loop
// --------------------------------------
void loop() {
  controller.run();
}