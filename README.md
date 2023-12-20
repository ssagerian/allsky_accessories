# allsky_accessories
=My Allsky camera senses the temperature and humidity inside the housing and controls an internal fan and dew heater.
A software service called temperatureMonitor.py sleeps for a minute then reads the temperature, humidity and the state of the fan and dew heater outputs. These values are written to a file which is used by the allsky software and added to the current image as part of the image overlay.

= GPIO assignments 
* Heater is on GPIO 17 (broadcom #) which controls a FET switch to switch on/off 12VDC to the nicrohire
* Fan is on GPIO 18 (broadcom #) which controls a FET switch to 5VDC fan 
* Si7020 uses I2C bus 1 (3.3 VDC device)

= Software needed
* pigpio library https://abyz.me.uk/rpi/pigpio/
* smbus2 python module
* temperatureMonitory.py 
* 

= pigpio
make sure you enable the service > sudo systemctl enable pigpiod 

= smbus2 
install smbus2 which is used by temperatureMonitor.py to read the si7020 I2C chip
* pip3 install smbus2
== you can install i2c-tools to debug your connections to the si chip
* sudo apt-get install i2c-tools
* sudo i2cdetect -y 1   # Use -y 0 for bus 0

= setup of the temperatureMonitory service
==Create a service file in /etc/systemd/system/allsky_accessories.service:
[Unit]
Description=Allsky accessory controller
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/allsky/path/to/temperatureMonitor.py
WorkingDirectory=/home/pi/allsky/
Restart=always
User=your_username

[Install]
WantedBy=multi-user.target





