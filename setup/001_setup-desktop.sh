################################################################################
### Minimal Desktop
################################################################################

# Latest Kernel and Latest Driver
apt -y install firmware-linux-nonfree firmware-realtek firmware-amd-graphics
# Simple Desktop
apt -y install --no-install-recommends xserver-xorg-core xserver-xorg
apt -y install --no-install-recommends gdm3 gnome-shell gnome-session
# Desktop tools
apt -y install gnome-control-center nautilus gnome-terminal gnome-bluetooth
# # Auto login
vi /etc/gdm3/daemon.conf
  [daemon]
  AutomaticLoginEnable = true
  AutomaticLogin = engineer
  TimedLoginEnable = true
  TimedLogin = engineer
  TimedLoginDelay = 10
# VNC Server
# apt -y install tigervnc-scraping-server
# su - engineer -c 'mkdir -p ~/.vnc'
# su - engineer -c 'vncpasswd'
# su - engineer -c 'x0vncserver -passwordfile ~/.vnc/passwd -display :0 >/dev/null 2>&1 &'

################################################################################
### Minimal Desktop with Google Chrome
################################################################################

apt -y install wget gnupg
echo 'deb [trusted=yes] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 1397BC53640DB551
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
apt -y update && apt -y install google-chrome-stable

################################################################################
### Minimal Desktop with VScode
################################################################################
###
# REFER : https://linuxize.com/post/how-to-install-visual-studio-code-on-debian-10/
apt install -y gnupg2 software-properties-common apt-transport-https curl
curl -sSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
apt -y update
apt -y install code
apt -y install git

################################################################################
### AnyDesk
################################################################################
wget -qO - https://keys.anydesk.com/repos/DEB-GPG-KEY | apt-key add -
echo "deb http://deb.anydesk.com/ all main" > /etc/apt/sources.list.d/anydesk-stable.list
apt -y update
apt -y install anydesk