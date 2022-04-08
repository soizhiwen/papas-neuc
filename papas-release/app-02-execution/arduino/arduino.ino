#include "implementation.h"

void setup()
{
    Serial.begin(115200);
    dxl.begin(1000000);
    dxl.setPortProtocolVersion(DXL_PROTOCOL_VERSION);

    my_servo.attach(servoPin);    // attaches the servo on pin 9 to the servo object
    pinMode(airPumpPin, OUTPUT);  // air pump
    pinMode(solenoidPin, OUTPUT); // solenoid

    for (int i = 0; i < DXL_ID_CNT; i++)
    {
        dxl.torqueOff(DXL_ID_LIST[i]);
        dxl.setOperatingMode(DXL_ID_LIST[i], OP_EXTENDED_POSITION);
    }

    // Fill the members of structure to syncWrite using internal packet buffer
    sw_infos.packet.p_buf = nullptr;
    sw_infos.packet.is_completed = false;
    sw_infos.addr = SW_START_ADDR;
    sw_infos.addr_length = SW_ADDR_LEN;
    sw_infos.p_xels = info_xels_sw;
    sw_infos.xel_count = 0;

    sw_data[0].goal_position = 0;
    sw_data[1].goal_position = 0;
    for (int i = 0; i < DXL_ID_CNT; i++)
    {
        info_xels_sw[i].id = DXL_ID_LIST[i];
        info_xels_sw[i].p_data = (uint8_t *)&sw_data[i].goal_position;
        sw_infos.xel_count++;
    }
    sw_infos.is_info_changed = true;
    setMaxVoltage(70);
    // initialize
    my_servo.write(180);
    digitalWrite(airPumpPin, HIGH);
    digitalWrite(solenoidPin, LOW);
    syncWrite(1023, -1023, 32, 0, 0, 40, 40);
    syncWrite(-1023, 1023, 32, 0, 0, 40, 40);
    syncWrite(1023, -1023, 32, 0, 0, 40, 40);
}

void loop()
{
    if (Serial.available() > 0)
    {
        if (flow_id == 0)
        {
            char buf[1];
            size_t n = Serial.readBytes(buf, 1);
            int temp_flow_id = int(buf[0]);
            if (temp_flow_id == 2)
            {
                flow_id = 2;
            }
            else if (temp_flow_id == 11)
            {
                flow_id = 0;
                // ID-1: Write present position
                // getPosition();
                left_pp = -1023;
                right_pp = 1023;
                int abs_left_pp = abs(left_pp);
                int abs_right_pp = abs(right_pp);
                int left_x = abs_left_pp % 255;
                int left_y = abs_left_pp / 255;
                int left_z = left_pp < 0 ? 2 : 1;
                int right_x = abs_right_pp % 255;
                int right_y = abs_right_pp / 255;
                int right_z = right_pp < 0 ? 2 : 1;
                byte arr[] = {left_x, left_y, left_z, right_x, right_y, right_z};
                Serial.write(1);
                Serial.write(arr, sizeof(arr));
            }
        }
        else if (flow_id == 2)
        {
            flow_id = 0;
            char buf[7];
            size_t n = Serial.readBytes(buf, 7);
            // extract the left and right angles
            int left_sign = 1;
            int right_sign = 1;
            if (int(buf[2]) == 2)
                left_sign = -1;
            if (int(buf[5]) == 2)
                right_sign = -1;
            int left_angle = (int(buf[0]) + (255 * int(buf[1]))) * left_sign;
            int right_angle = (int(buf[3]) + (255 * int(buf[4]))) * right_sign;
            syncWrite(-1023, 1023, 32, 0, 0, 40, 40);
            syncWrite(left_angle, right_angle, 64, 0, 32, 25, 25);
            delay(300);
            // control micro servo and sucker
            digitalWrite(airPumpPin, LOW);
            digitalWrite(solenoidPin, HIGH); // suck
            my_servo.write(0);               // down
            delay(700);
            my_servo.write(180); // up
            delay(400);
            syncWrite(-1023, 1023, 16, 0, 0, 40, 40);
            syncWrite(1023, -1023, 32, 0, 0, 40, 40);
            int desired_location = int(buf[6]);
            if (desired_location == 0)
                syncWrite(47, -1099, 128, 0, 64, 40, 40);
            else if (desired_location == 1)
                syncWrite(314, -685, 128, 0, 64, 40, 40);
            else if (desired_location == 2)
                syncWrite(685, -314, 128, 0, 64, 40, 40);
            else if (desired_location == 3)
                syncWrite(1099, -47, 128, 0, 64, 40, 40);
            else if (desired_location == 4)
                syncWrite(651, -1121, 128, 0, 64, 40, 40);
            else if (desired_location == 5)
                syncWrite(1121, -651, 128, 0, 64, 40, 40);
            delay(300);
            // place shape at desired location
            my_servo.write(0); // down
            delay(400);
            digitalWrite(airPumpPin, HIGH);
            digitalWrite(solenoidPin, LOW); // release
            delay(250);
            my_servo.write(180); // up
            delay(400);
            syncWrite(1023, -1023, 16, 0, 0, 40, 40);
            // ID-12: Write done
            Serial.write(12);
        }
    }

    // getPID();
    // getTemperature();
}
