#include <Arduino.h>

float counter = 0.0;

void setup() {
  Serial.begin(19200);     // Match your SerialManager baud rate
  delay(2000);             // Give time for Serial to connect
}

void loop() {
  // --- Simulate accelerometer data (m/s^2) ---
  float ax = 1.0 * sin(counter / 10.0) + random(-5, 5) / 100.0;   // ±0.05 noise
  float ay = 1.0 * cos(counter / 10.0) + random(-5, 5) / 100.0;
  float az = 9.81 + random(-10, 10) / 100.0;                      // around gravity

  // --- Simulate gyroscope data (rad/s) ---
  float gx = 0.5 * sin(counter / 15.0) + random(-2, 2) / 100.0;
  float gy = 0.5 * cos(counter / 15.0) + random(-2, 2) / 100.0;
  float gz = random(-5, 5) / 100.0;

  // --- Send data as CSV string ---
  Serial.print(ax, 3); Serial.print(",");
  Serial.print(ay, 3); Serial.print(",");
  Serial.print(az, 3); Serial.print(",");
  Serial.print(gx, 3); Serial.print(",");
  Serial.print(gy, 3); Serial.print(",");
  Serial.println(gz, 3);

  // Optional: print debug to Serial Monitor (same output anyway)
  // Serial.println("[DEBUG] IMU sent");

  counter += 1.0;
  delay(1000);  // Send every 1 second
}
