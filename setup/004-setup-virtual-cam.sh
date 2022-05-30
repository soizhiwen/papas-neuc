### Step 1 : Setup Motion
apt -y install motion
mkdir -p /var/log/motion/
chmod 777 /var/log/motion/
mkdir -p /var/lib/motion/
chmod 777 /var/lib/motion/

sed -i 's/^width 640/width 1280/g' /etc/motion/motion.conf
sed -i 's/^height 480/height 720/g' /etc/motion/motion.conf
sed -i 's/^framerate 15/framerate 30/g' /etc/motion/motion.conf
sed -i 's/^stream_localhost on/stream_localhost off/g' /etc/motion/motion.conf
sed -i 's/^webcontrol_localhost on/webcontrol_localhost off/g' /etc/motion/motion.conf
sed -i 's/^movie_output on/movie_output off/g' /etc/motion/motion.conf
# sed -i 's/^daemon off/daemon on/g' /etc/motion/motion.conf

nano /etc/motion/motion.conf
# stream_quality 100
# stream_maxrate 100
# videodevice /dev/video6

systemctl start motion
systemctl restart motion
systemctl stop motion

### Step 2 : Setup v4l2loopback
apt -y install v4l2loopback-dkms v4l2loopback-utils \
    gstreamer1.0-tools gstreamer1.0-plugins-good libopencv-dev \
    build-essential

### For RaspberryPi, install RPi kernel header
apt -y install raspberrypi-kernel-headers

modprobe v4l2loopback \
	devices=1 exclusive_caps=1 video_nr=6 \
	card_label="OpenCV Camera"

v4l2-ctl --list-devices -d6