# allsky_accessories
My Allsky camera senses the temperature and humidity inside the housing and controls an internal fan and dew heater.
A software service called temperatureMonitor.py sleeps for a minute then reads the temperature, humidity and the state of the fan and dew heater outputs. These values are written to a file which is used by the allsky software and added to the current image as part of the image overlay.

## GPIO assignments 
* Heater is on GPIO 17 (broadcom #) which controls a FET switch to switch on/off 12VDC to the nicrohire
* Fan is on GPIO 18 (broadcom #) which controls a FET switch to 5VDC fan 
* Si7020 uses I2C bus 1 (3.3 VDC device)

# Software needed
* pigpio library https://abyz.me.uk/rpi/pigpio/
* smbus2 python module
* temperatureMonitory.py 
* 

# pigpio
make sure you enable the service > sudo systemctl enable pigpiod 

# smbus2 
install smbus2 which is used by temperatureMonitor.py to read the si7020 I2C chip
* pip3 install smbus2
## i2c tools
you can install i2c-tools to debug your connections to the si chip
* sudo apt-get install i2c-tools
* sudo i2cdetect -y 1   # Use -y 0 for bus 0

#Setup of the temperatureMonitory service
* copy the temperatureMonitory.service to /etc/systemd/system/
* enable the service
** sudo systemctl enable temperatureMonitor
* start the service
** sudo systemctrl start temperatureMonitor
* status the temperatureMonitor
** sudo systemctrl status temperatureMonitor
#setup of additional storage for images using usb thumb drive
You can permanaently add a usb thumb drive as more storage for your allsky
## determine UUID of the device
Plug in the device and then execut the following to get the UUID info
* lsblk -o NAME,UUID
make a mount point for the thumbdrive
* sudo mkdir /mnt/myusbdrive
edit the file system table
* sudo nano /etc/fstab
add an entry into fstab
*PARTUUID=your-usb-drive-uuid /mnt/myusbdrive ntfs-3g defaults,auto,users,rw,nofail,uid=1000,gid=1000 0 0
now mount the drive
* sudo mount -a
now check that the drive is active
* df -h








