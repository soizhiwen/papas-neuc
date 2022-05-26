###############################################################################
### Arduino-CLI Program
###############################################################################

### Step 1 : Install Arduino-CLI
# REFER : https://arduino.github.io/arduino-cli/installation/
apt -y install curl wget
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=/usr/bin sh
arduino-cli version

### Step 2 : Prepare Board Library
arduino-cli core update-index
arduino-cli core install arduino:samd
arduino-cli core list

###############################################################################
### Enable Serial Debug and Remote Sync
###############################################################################

### Serial Debuging
# Install
apt -y install picocom
# Enter Serial Com
picocom -b 9600 -r -l /dev/ttyACM0
# Quit Serial Com
# To exit picocom, use CTRL-A followed by CTRL-X.

###############################################################################
### Other Libraries
###############################################################################

### Install Related Library
arduino-cli lib update-index
arduino-cli lib install DynamixelShield Servo

###############################################################################
### Detect Hardware
###############################################################################
apt -y install hwinfo

### Senario 1.A : Plug in Arduino MKR WiFI 1010 as NORMAL start up mode
hwinfo | grep Arduino
#   Model: "Arduino SA Arduino MKR WiFi 1010"
#   Vendor: usb 0x2341 "Arduino SA"
#   Device: usb 0x8054 "Arduino MKR WiFi 1010"

### Senario 1.B : Plug in Arduino MKR WiFI 1010 as BOOTOADER start up mode
hwinfo | grep Arduino
#   Model: "Arduino SA Arduino MKR WiFi 1010"
#   Vendor: usb 0x2341 "Arduino SA"
#   Device: usb 0x0054 "Arduino MKR WiFi 1010"

###############################################################################
### Timestamp for PICOCOM
###############################################################################
apt -y install screen moreutils
picocom -b 9600 -r -l /dev/ttyACM0 | ts