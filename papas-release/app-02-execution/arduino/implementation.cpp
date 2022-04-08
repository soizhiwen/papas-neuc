#include "implementation.h"

sw_data_t sw_data[DXL_ID_CNT];
DYNAMIXEL::InfoSyncWriteInst_t sw_infos;
DYNAMIXEL::XELInfoSyncWrite_t info_xels_sw[DXL_ID_CNT];
DynamixelShield dxl;
Servo my_servo;
int flow_id = 0;

int left_pp = 0;
int right_pp = 0;

void setPID(int p_gain, int i_gain, int d_gain)
{
    for (int i = 0; i < DXL_ID_CNT; i++)
    {
        dxl.writeControlTableItem(P_GAIN, DXL_ID_LIST[i], p_gain);
        dxl.writeControlTableItem(I_GAIN, DXL_ID_LIST[i], i_gain);
        dxl.writeControlTableItem(D_GAIN, DXL_ID_LIST[i], d_gain);
    }
}

void setMovingSpeed(int left_ms, int right_ms)
{
    dxl.writeControlTableItem(MOVING_SPEED, DXL_ID_LIST[0], left_ms);
    dxl.writeControlTableItem(MOVING_SPEED, DXL_ID_LIST[1], right_ms);
}

void syncWrite(int left_gp, int right_gp, int p_gain, int i_gain, int d_gain, int left_ms, int right_ms)
{
    setMaxVoltage(120);
    setPID(p_gain, i_gain, d_gain);
    setMovingSpeed(left_ms, right_ms);

    sw_data[0].goal_position = left_gp;
    sw_data[1].goal_position = right_gp;
    sw_infos.is_info_changed = true;

    dxl.syncWrite(&sw_infos);
    while (isMovingLeft() || isMovingRight())
        ;
    delay(100);
    setMaxVoltage(70);
    setTorqueOff();
}

void getPosition()
{
    left_pp = dxl.getPresentPosition(DXL_ID_LIST[0]);
    right_pp = dxl.getPresentPosition(DXL_ID_LIST[1]);
    LOG_PRINT("Left Present Position: ");
    LOG_PRINTLN(left_pp);
    LOG_PRINT("Right Present Position: ");
    LOG_PRINTLN(right_pp);
}

void setMaxVoltage(int volt)
{
    for (int i = 0; i < DXL_ID_CNT; i++)
        dxl.writeControlTableItem(MAX_VOLTAGE_LIMIT, DXL_ID_LIST[i], volt);
}

void setTorqueOff()
{
    for (int i = 0; i < DXL_ID_CNT; i++)
        dxl.torqueOff(DXL_ID_LIST[i]);
}

void getPID()
{
    for (int i = 0; i < DXL_ID_CNT; i++)
    {
        LOG_PRINT((String) "P_GAIN [" + DXL_ID_LIST[i] + "]: ");
        LOG_PRINTLN(dxl.readControlTableItem(P_GAIN, DXL_ID_LIST[i]));

        LOG_PRINT((String) "I_GAIN [" + DXL_ID_LIST[i] + "]: ");
        LOG_PRINTLN(dxl.readControlTableItem(I_GAIN, DXL_ID_LIST[i]));

        LOG_PRINT((String) "D_GAIN [" + DXL_ID_LIST[i] + "]: ");
        LOG_PRINTLN(dxl.readControlTableItem(D_GAIN, DXL_ID_LIST[i]));
    }
}

void getTemperature()
{
    for (int i = 0; i < DXL_ID_CNT; i++)
    {
        LOG_PRINT((String) "PRESENT_TEMPERATURE [" + DXL_ID_LIST[i] + "]: ");
        LOG_PRINTLN(dxl.readControlTableItem(PRESENT_TEMPERATURE, DXL_ID_LIST[i]));
    }
}

int isMovingLeft()
{
    return dxl.readControlTableItem(MOVING, DXL_ID_LIST[0]);
}

int isMovingRight()
{
    return dxl.readControlTableItem(MOVING, DXL_ID_LIST[1]);
}