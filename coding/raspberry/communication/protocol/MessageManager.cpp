#include <iostream>
#include <stdlib.h>
#include "MessageManager.h"

#include <pybind11/pybind11.h>

namespace py = pybind11;

uint8_t MessageManager::packPayload() {
  uint8_t *ptr = payload;
  
  memcpy(ptr, &mask, sizeof(mask)); ptr += sizeof(mask);
  
  if (mask & MOTOR_ENCODER_MASK) { 
    memcpy(ptr, data.motor_encoders, sizeof(uint16_t) * 4); ptr += sizeof(uint16_t) * 4; len++; 
    mask &= ~MOTOR_ENCODER_MASK;            // Clear MOTOR_ENCODER_BIT after packing
  }
  if (mask & HOME_SWITCH_MASK) { 
    memcpy(ptr, data.home_switches, sizeof(bool) * 4); ptr += sizeof(bool) * 4; len++; 
    mask &= ~HOME_SWITCH_MASK;              // Clear HOME_SWITCH_BIT after packing
  }
  if (mask & POTENTIOMETER_MASK) { 
    memcpy(ptr, data.potentiometers, sizeof(uint16_t) * 2); ptr += sizeof(uint16_t) * 2; len++; 
    mask &= ~POTENTIOMETER_MASK;            // Clear POTENTIOMETER_BIT after packing
  }
  if (mask & REF_DIODE_MASK) { 
    memcpy(ptr, &data.ref_diode, sizeof(uint16_t)); ptr += sizeof(uint16_t); len++; 
    mask &= ~REF_DIODE_MASK;                // Clear REF_DIODE_BIT after packing
  }
  if (mask & TEMP_SENSOR_MASK) { 
    memcpy(ptr, &data.temp_sensor, sizeof(float)); ptr += sizeof(float); len++;
    mask &= ~TEMP_SENSOR_MASK;              // Clear TEMP_SENSOR_BIT after packing
  }
  if (mask & IMU_MASK) { 
    memcpy(ptr, data.imu, sizeof(float) * 6); ptr += sizeof(float) * 6; len++;
    mask &= ~IMU_MASK;                      // Clear IMU_BIT after packing
  }

  return ptr - payload;
}
/*


void MessageManager::sendMessage() {
  uint8_t modified_mask = mask; // Local copy to track which fields are sent
  len = packPayload(modified_mask);

  uart.write(START_BYTE);
  uart.write(mask); 
  uart.write(len);
  uart.write(payload, len);

  uint8_t totalBytes = 1 + 1 + 1 + len;    // Start + mask + length + payload
  Serial.print("Sending total bytes: ");
  Serial.println(totalBytes);

  mask = modified_mask; // Update the class mask after sending
}
*/


void MessageManager::loadData() {
  uint8_t *ptr = payload;

  memcpy(&mask, ptr, sizeof(mask)); ptr += sizeof(mask);

  if (mask & MOTOR_ENCODER_MASK) {
    memcpy(data.motor_encoders, ptr, sizeof(uint16_t) * 4); ptr += sizeof(uint16_t) * 4;
  }
  if (mask & HOME_SWITCH_MASK) {
    memcpy(data.home_switches, ptr, sizeof(bool) * 4); ptr += sizeof(bool) * 4;
  }
  if (mask & POTENTIOMETER_MASK) {
    memcpy(data.potentiometers, ptr, sizeof(uint16_t) * 2); ptr += sizeof(uint16_t) * 2;
  }
  if (mask & REF_DIODE_MASK) {
    memcpy(&data.ref_diode, ptr, sizeof(uint16_t)); ptr += sizeof(uint16_t);
  }
  if (mask & TEMP_SENSOR_MASK) {
    memcpy(&data.temp_sensor, ptr, sizeof(float)); ptr += sizeof(float);
  }
  if (mask & IMU_MASK) {
    memcpy(data.imu, ptr, sizeof(float) * 6); ptr += sizeof(float) * 6;
  }
}
/*
void MessageManager::readMessage() {
  while (uart.available()) {
    uint8_t b = uart.read();
    switch (readState) {
      case WAIT_FOR_START:
        if (b == START_BYTE) readState = WAIT_FOR_MASK;
        break;

      case WAIT_FOR_MASK:
        mask = b;
        readState = WAIT_FOR_LENGTH;
        break;

      case WAIT_FOR_LENGTH:
        len = b;
        payloadIndex = 0;
        readState = WAIT_FOR_PAYLOAD;
        break;

      case WAIT_FOR_PAYLOAD:
        payload[payloadIndex++] = b;
        if (payloadIndex >= len) { // full packet received
          loadData();
          readState = WAIT_FOR_START;
        }
        break;
    }
  }
}
*/
static size_t payloadIndex = 0;

void MessageManager::fillPayload(uint8_t byte) {

  if (byte == END_BYTE){
    payloadIndex = 0;
    return;
  }
  
  payload[payloadIndex++] = byte;
}

void MessageManager::readDataFromString(const char* values[]) {

    uint8_t valuesIndex = 0;

    std::cout << "Mask: " << values[0] << std::endl;

    mask = static_cast<uint8_t>(atoi(values[valuesIndex++]));

    std::cout << "=========================MASK=========================: " << (int)mask << std::endl;

    if (mask & MOTOR_ENCODER_MASK) {
      for (int i = 0; i < 4; i++) {
        data.motor_encoders[i] = static_cast<uint16_t>(atoi(values[valuesIndex++]));
        std::cout << "Motor encoder[" << i << "]: " << data.motor_encoders[i] << std::endl;
      }
    }
    if (mask & HOME_SWITCH_MASK){
      for (size_t i = 0; i < 4; i++) {
        data.home_switches[i] = static_cast<bool>(atoi(values[valuesIndex++]));
        std::cout << "Home switch[" << i << "]: " << data.home_switches[i] << std::endl;
      }
    }
    if (mask & POTENTIOMETER_MASK) {
      for (int i = 0; i < 2; i++) {
        data.potentiometers[i] = static_cast<uint16_t>(atoi(values[valuesIndex++]));
        std::cout << "Potentiometer[" << i << "]: " << data.potentiometers[i] << std::endl;
      }
    } 
    if (mask & REF_DIODE_MASK) {
      data.ref_diode = static_cast<uint16_t>(atoi(values[valuesIndex++]));
      std::cout << "Ref diode: " << data.ref_diode << std::endl;
    }
    if (mask & TEMP_SENSOR_MASK) {
      data.temp_sensor = static_cast<float>(atof(values[valuesIndex++]));
      std::cout << "Temp sensor: " << data.temp_sensor << std::endl;
    }
    if (mask & IMU_MASK){
      for (size_t i = 0; i < 6; i++) {
        data.imu[i] = static_cast<float>(atof(values[valuesIndex++]));
      }
    }
}

void MessageManager::setMotorEncoder(const uint16_t motor_encoders[4]) {
  std::memcpy(data.motor_encoders, motor_encoders, sizeof(uint16_t) * 4);
  mask |= MOTOR_ENCODER_MASK;
}

void MessageManager::setHomeSwitches(const bool home_switches[4]) {
  std::memcpy(data.home_switches, home_switches, sizeof(bool) * 4);
  mask |= HOME_SWITCH_MASK;
}

void MessageManager::setPotentiometers(const uint16_t potentiometers[2]) {
  std::memcpy(data.potentiometers, potentiometers, sizeof(uint16_t) * 2);
  mask |= POTENTIOMETER_MASK;
}

void MessageManager::setRefDiode(const uint16_t ref_diode) {
  //data.ref_diode = ref_diode;
  std::memcpy(&data.ref_diode, &ref_diode, sizeof(uint16_t));
  mask |= REF_DIODE_MASK;
}

void MessageManager::setTempSensor(const float temp_sensor) {
  //data.temp_sensor = temp_sensor;
  std::memcpy(&data.temp_sensor, &temp_sensor, sizeof(float));
  mask |= TEMP_SENSOR_MASK;
}

void MessageManager::setImu(const float imu[6]) {
  std::memcpy(data.imu, imu, sizeof(float) * 6);
  /*std::cout << "IMU values in C++: ";
  for (int i = 0; i < 6; i++) { 
    std::cout << data.imu[i] << " ";
  }
  std::cout << std::endl;*/
  mask |= IMU_MASK;
}

MessageManager::Sensors& MessageManager::getSensors() {
  return data;
}

uint8_t* MessageManager::getPayload() {
    return payload;
}