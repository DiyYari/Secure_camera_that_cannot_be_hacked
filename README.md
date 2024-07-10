https://www.realvnc.com/en/connect/download/viewer/?lai_sr=5-9&lai_sl=l

commands for setting up remote access to the system

Sudo apt-get install realvnc-vnc-server realvnc-vnc-viewer

Ifconfig (IP address check)


these commands must be entered in the Rasberry PI environment to install the necessary libraries

sudo apt update

sudo apt upgrade -y

sudo apt install python3-pip -y

sudo apt install -y python3-libcamera python3-kms++

pip3 install Flask picamera2 adafruit-circuitpython-pca9685 adafruit-circuitpython-motor

#if there is a problem with the installation

sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED

#then run it again

pip3 install Flask picamera2 adafruit-circuitpython-pca9685 adafruit-circuitpython-motor

sudo apt install -y i2c-tools python3-smbus

save the camera.py file to a new folder for example "camera"

index.html to the folder camera/templates/index.html, 

then do: python3 camera.py
