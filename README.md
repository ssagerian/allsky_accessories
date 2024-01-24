# allsky_accessories
My Allsky camera senses the temperature and humidity inside the housing and controls an internal fan and dew heater.
A software service called temperatureMonitor.py sleeps for a minute then reads the temperature, humidity and the state of the fan and dew heater outputs. These values are written to a file which is used by the allsky software and added to the current image as part of the image overlay.

## GPIO assignments 
* Heater is on GPIO 17 (broadcom #) which controls a FET switch to switch on/off 12VDC to the nicrohire
* Fan is on GPIO 18 (broadcom #) which controls a FET switch to 5VDC fan 
* Si7020 uses I2C bus 1 (3.3 VDC device)



| funct  | Pin                | Pin    | funct  |
|--------|--------------------|--------|--------|
| 3.3VDC | 1                  | 2      | 5VDC   |
| SDA    | 3                  | 4      | 5VDC   |
| SCL   | 5                  | 6      | ...   |
| ...    | 7                | 8    | ...    |
| GND    | 9                | 10    | ...    |
| HEATER    | 11                | 12    | FAN    |
| ...    | 13                | 14    | GND    |
| ...    | 15                | 16    | ...    |
| ...    | 17                | 18    | ...    |
| ...    | 19                | 20    | GND    |
| ...    | 21                | 22    | ...    |
| ...    | 23                | 24    | ...    |
| GND    | 25                | 26    | ...    |
| ...    | 27                | 28    | ...    |
| ...    | 29                | 30    | GND    |
| ...    | 31                | 32    | ...    |
| ...    | 33                | 34    | GND    |
| ...    | 35                | 36    | ...    |
| ...    | 37                | 38    | ...    |
| GND    | 39                | 40    | ...    |


Colors for I2C bus hookup

| funct | Color |
|-------|-------|
| VCC | YELLOW |
| GND | ORANGE |
| SCL | RED |
| SDA| BROWN |

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

# Notes about temperature Monitor
It now has the following functions
* read temp and humidity from si7020 chip
* stores those data items in a json file in the overlays/extra folder of the allsky system
* plots the data onto a graph and saves the graph for the overlay
* at midnite it saves all the temp, humidity with individual time stamps to the previous day's image folder
  ** the intent here is that the T&H data will get archived with the images
* at midnite it restarts accumulating T&H data for the current day
* 






