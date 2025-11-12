#ifndef _MSG_MANAGER_H_
#define _MSG_MANAGER_H_

//#include <Arduino.h>
#include <stdint.h>

/* TO ADD A SENSOR:

In this file:
1. Define the sensor bit and mask
2. Add the sensor to the Sensors struct
3. (Optional) Update the size of mask variable if number of sensors exceed current number of bits
4. (Optional) Update the size of payload array if max payload size exceed current size

In MessageManager.cpp:
3. Update the packPayload function to include new sensor data 
Pattern:
  if (local_mask & NEW_SENSOR_MASK) { 
    memcpy(ptr, data.new_sensor, sizeof(NEW_SENSOR_TYPE) * N); ptr += sizeof(NEW_SENSOR_TYPE) * N; 
    local_mask &= ~NEW_SENSOR_MASK;            // Clear NEW_SENSOR_BIT after packing
  }
4. Update the loadData function to include new sensor data
Pattern:
  if (mask & NEW_SENSOR_MASK) {
    memcpy(data.new_sensor, ptr, sizeof(NEW_SENSOR_TYPE) * N); ptr += sizeof(NEW_SENSOR_TYPE) * N;
    // (Optional) Print the new sensor data for debugging
  }

*/

#define MOTOR_ENCODER_BIT       0
#define HOME_SWITCH_BIT         1
#define POTENTIOMETER_BIT       2
#define REF_DIODE_BIT           3
#define TEMP_SENSOR_BIT         4
#define IMU_BIT                 5

#define MOTOR_ENCODER_MASK      (1 << MOTOR_ENCODER_BIT)
#define HOME_SWITCH_MASK        (1 << HOME_SWITCH_BIT)
#define POTENTIOMETER_MASK      (1 << POTENTIOMETER_BIT)
#define REF_DIODE_MASK          (1 << REF_DIODE_BIT)
#define TEMP_SENSOR_MASK        (1 << TEMP_SENSOR_BIT)
#define IMU_MASK                (1 << IMU_BIT)

#define START_BYTE              0xAA
#define END_BYTE                0xBB

class MessageManager {

    public: 
    //HardwareSerial &uart = Serial2;           // REMOVE

    uint8_t mask = 0;
    uint8_t payload[64];

    MessageManager()=default; 
    ~MessageManager()=default;

    //void sendMessage();                       // REMOVE
    //void readMessage();                       // REMOVE

    uint8_t packPayload();
    void fillPayload(uint8_t);
    void loadData();
    uint8_t* getPayload();
    void readDataFromString(const char* values[]);

    void setMotorEncoder(const uint16_t motor_encoders[4]);
    void setHomeSwitches(const bool home_switches[4]);
    void setPotentiometers(const uint16_t potentiometers[2]);
    void setRefDiode(const uint16_t ref_diode);
    void setTempSensor(const float temp_sensor);
    void setImu(const float imu[6]);

    #pragma pack(push, 1)
    struct Sensors {
        uint16_t motor_encoders[4];
        bool home_switches[4]; //Switched from bools --> uint8_t
        uint16_t potentiometers[2];
        uint16_t ref_diode;
        float temp_sensor;
        float imu[6];
    };
    #pragma pack(pop)

    Sensors data;

    Sensors& getSensors();

    uint8_t len = 0;
    private:

    //enum ReadState { WAIT_FOR_START, WAIT_FOR_MASK, WAIT_FOR_LENGTH, WAIT_FOR_PAYLOAD };
    //ReadState readState = WAIT_FOR_START;     // REMOVE
    //size_t payloadIndex = 0;                  // REMOVE
};

#endif //_MSG_MANAGER_H_