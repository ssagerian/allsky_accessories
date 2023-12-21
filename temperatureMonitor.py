
import time
import smbus
import json
import syslog

address = 0x40
temperatureCmd = 0xF3
humidityCmd = 0xF5

bus = smbus.SMBus(1)

# init chip
bus.write_byte(address, 0xFE) # reset sensor
time.sleep(1)
bus.write_byte_data(address,0xE6, 0x3B) # heater on Temp Resolution == 12 bits, RH= 8 bits

# class for holding sensor data and converting to json
class SensorData:
    def __init__(self, temperature, humidity, dew_heater_status, fan_status):
        self.data_dict = {}
        self.data_dict['HS_TIME_STAMP'] = {'value': 0}
        self.data_dict['HS_TEMPERATURE'] = {'value': temperature, 'expires': 600}
        self.data_dict['HS_HUMIDITY'] = {'value': humidity, 'expires': 600}
        self.data_dict['HS_DEW_HEATER_STATUS'] = {'value': dew_heater_status, 'expires': 600}
        self.data_dict['HS_FAN_STATUS'] = {'value': fan_status, 'expires': 600}

    def get_data_json(self):
        return json.dumps(self.data_dict, indent=2)

    def save_to_json(self, filename):
        with open(filename, 'w') as json_file:
            json.dump(self.data_dict, json_file, indent=4)


def getTemperature():
    temp = bus.read_word_data(address,0xE0) # read temp from last humidity conversion
    temp = (temp/256)+ int((temp%256)*256)  #swap msb and lsb 
    #temp = int(temp/256)+ ((temp%256)*256)  #swap msb and lsb 
#   Maybe swapped per http://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/plain/Documentation/i2c/smbus-protocol
    temperature = ((175.72 * temp)/65536) - 46.85
    return temperature

def celiusToFahrenheit(celius):
    fah = celius * 1.80  + 32 
    return fah

def fahrenheitToCelius(fahrenheit):
    celius = (fahrenheit - 32) * 0.556
    return celius

def getHumidity():
    humd = bus.read_word_data(address, 0xE5)
    humd = int(humd/256) + ((humd % 256)*256)  #swap msb and lsb
    humidity = ((125 * humd)/65536) - 6
    return humidity

def get_humidity_and_temperatureF():    # Call temperature and humidity functions
    humidity = getHumidity()
    temperature = getTemperature()
    temperature = celiusToFahrenheit(temperature)
    return humidity, temperature
#
def main():
    while True:
        # Call temperature and humidity functions
        humidity, temperature = get_humidity_and_temperatureF()

        # Round values to one significant digit
        temperature_rounded = round(temperature, 1)
        humidity_rounded = round(humidity, 1)
        # this needs to change based on actual path
        file_path = '/home/pi/allsky/config/overlay/extra/sensor_data.json'

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        sensor_data = SensorData(temperature_rounded, humidity_rounded, 'ON', 'ON')
        sensor_data.data_dict['HS_TIME_STAMP'] = timestamp
        # Update data dictionary
        sensor_data.save_to_json(file_path)
        syslog.syslog(syslog.LOG_INFO, f"Allsky Temperature: {temperature_rounded} F")
        #with open(file_path, 'a') as file:
        #    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        #    file.write(f"{timestamp} - Temperature: {temperature_rounded} °C, Humidity: {humidity_rounded}%\n")
        #    print(f"{timestamp} - Temperature: {temperature} °F, Humidity: {humidity}%\n")

        # Sleep for a minute
        time.sleep(60)

if __name__ == "__main__":
    main()

