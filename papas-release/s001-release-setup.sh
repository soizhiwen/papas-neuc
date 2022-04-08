#!/bin/bash

#####################################################################
### Papas Release
#####################################################################

arduino-cli board list

### app-01-camera-calibration
# Open new terminal
su -
modprobe v4l2loopback \
	devices=1 exclusive_caps=1 video_nr=6 \
	card_label="OpenCV Camera"
v4l2-ctl --list-devices -d6
source /usr/local/bin/venv/bin/activate
cd /home/engineer/papas/papas-release/app-01-camera-calibration/python
python main.py

# Open new terminal
motion


### app-02-execution
# Open new terminal
su -
modprobe v4l2loopback \
	devices=1 exclusive_caps=1 video_nr=6 \
	card_label="OpenCV Camera"
v4l2-ctl --list-devices -d6
cd /home/engineer/papas/papas-release/app-02-execution
arduino-cli compile --fqbn arduino:samd:mkrwifi1010 arduino
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:samd:mkrwifi1010 arduino

# Open new terminal
source /usr/local/bin/venv/bin/activate
cd /home/engineer/papas/papas-release/app-02-execution/python
python main.py