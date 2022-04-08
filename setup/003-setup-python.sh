################################################################################
### PYTHON ### PYTHON ### PYTHON ### PYTHON ### PYTHON ### PYTHON ### PYTHON ###
################################################################################

### As ROOT : Install Programming Language - Python
su -
apt -y install build-essential zlib1g-dev libncurses5-dev libgdbm-dev \
    libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
cd ~
wget https://www.python.org/ftp/python/3.10.4/Python-3.10.4.tgz
tar -xf Python-3.10.4.tgz
cd Python-3.10.4
./configure --enable-optimizations
make -j$(nproc)
make altinstall
cd ~
rm -rf Python-3.10.4
rm -rf Python-3.10.4.tgz

### As ROOT : Check it.
# python3 --version
python3 --version
python3.10 --version
python3.10 -m pip install --upgrade pip
python3.10 -m pip install virtualenv

### As NORMAL user : Prepare a Virtual Environment for Python
which virtualenv
which python3.10
virtualenv -p /usr/local/bin/python3.10 venv
# Activate VIRTUALENV
source /usr/local/bin/venv/bin/activate
python3.10 -m pip install --upgrade pip
python3.10 -m pip install opencv-contrib-python-headless pyserial numpy scipy
python3.10 -c "import cv2; print(cv2.__version__)"

