#ifndef IMPLEMENTATION_H
#define IMPLEMENTATION_H

#include <DynamixelShield.h>
#include <Servo.h>

// #define DEBUG 1
#ifdef DEBUG
#define LOG_PRINT(x) Serial.print(x)
#define LOG_PRINTLN(x) Serial.println(x)
#else
#define LOG_PRINT(x)
#define LOG_PRINTLN(x)
#endif

using namespace ControlTableItem;

// Structures
typedef struct sw_data
{
    int goal_position;
} __attribute__((packed)) sw_data_t;

// Constants
const int servoPin = 9;
const int airPumpPin = 2;
const int solenoidPin = 3;

const float DXL_PROTOCOL_VERSION = 1.0;
const uint8_t DXL_ID_CNT = 2;
const uint8_t DXL_ID_LIST[DXL_ID_CNT] = {3, 2};

const uint16_t SW_START_ADDR = 30; //Goal position
const uint16_t SW_ADDR_LEN = 2;

// Global Variables
extern sw_data_t sw_data[DXL_ID_CNT];
extern DYNAMIXEL::InfoSyncWriteInst_t sw_infos;
extern DYNAMIXEL::XELInfoSyncWrite_t info_xels_sw[DXL_ID_CNT];
extern DynamixelShield dxl;
extern Servo my_servo;
extern int flow_id;
extern int left_pp;
extern int right_pp;


// Function Declaration
void setPID(int p_gain, int i_gain, int d_gain);
void setMovingSpeed(int left_ms, int right_ms);
void setMaxVoltage(int volt);
void setTorqueOff();
void getPosition();
void getPID();
void getTemperature();
int isMovingLeft();
int isMovingRight();
void syncWrite(int left_gp, int right_gp, int p_gain, int i_gain, int d_gain, int left_ms, int right_ms);

#endif