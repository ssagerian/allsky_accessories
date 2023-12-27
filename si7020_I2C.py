import smbus
import time
import syslog


TEMPERATURE_COMMAND = 0xF3
HUMIDITY_COMMAND = 0xF5


class si7020_I2C:
    def __init__(self, address=0x40):
        heater_map = {0: "OFF", 1: "ON"}
        vdd_map = {0: "OK", 1: "LOW!"}
        resolution_mapping = {
       	    (0, 0): "RH: 12 bit, Temp: 14 bit",
            (0, 1): "RH: 8 bit, Temp: 12 bit",
            (1, 0): "RH: 10 bit, Temp: 13 bit",
            (1, 1): "RH: 11 bit, Temp: 11 bit",
        }
        try:
            # Your existing initialization code here

            self.address = address
            self.temperatureCmd = TEMPERATURE_COMMAND
            self.humidityCmd = HUMIDITY_COMMAND
            self.bus = smbus.SMBus(1)
            try:
                # init chip
                self.bus.write_byte(self.address, 0xFE)  # reset sensor
                time.sleep(1)
                self.bus.write_byte_data(self.address, 0xE6, 0x04)  # heater on Temp Resolution == 12 bits, RH= 8 bits
                time.sleep(1)
                read_data = self.bus.read_byte_data(self.address, 0xE7)  # read register 1
                heater_state = heater_map.get(((read_data & 0x04) >> 2), "?")
                vdd_status = vdd_map.get(((read_data & 0x40) >> 5), "?")
                rh_resolution = (read_data & 0x80) >> 6
                temp_resolution = read_data & 0x01
                resolution_description = resolution_mapping.get((rh_resolution, temp_resolution), "Unknown Resolution")
                print(f"Si7020:VDD {vdd_status} heater {heater_state} bit resolution {resolution_description}")
                syslog.syslog(syslog.LOG_INFO, f"Si7020:VDD {vdd_status} heater {heater_state} bit resolution {resolution_description}")

            except IOError as e:
                print(f"1 Failed to initialize si7020 I2C device: {e}")
                exit(1)
        except Exception as e:
            print(f"2 Error initializing si7020_I2C: {e}")
            exit(1)

    def get_temperature(self):
        temp = self.bus.read_word_data(self.address, 0xE0)  # read temp from last humidity conversion
        #temp = (temp / 256) + int((temp % 256) * 256)  # swap msb and lsb
        temperature = ((175.72 * temp) / 65536) - 46.85
        return temperature

    @staticmethod
    def celsius_to_fahrenheit(celsius):
        fah = celsius * 1.80 + 32
        return fah

    @staticmethod
    def fahrenheit_to_celsius(fahrenheit):
        celsius = (fahrenheit - 32) * 0.556
        return celsius

    def get_humidity(self):
        humd = self.bus.read_word_data(self.address, 0xE5)
        #humd = int(humd / 256) + ((humd % 256) * 256)  # swap msb and lsb
        humidity = ((125 * humd) / 65536) - 6
        return humidity

    def get_humidity_and_temperatureF(self):  # Call temperature and humidity functions
        humidity = self.get_humidity()
        temperature = self.get_temperature()
        temperature_f = si7020_I2C.celsius_to_fahrenheit(temperature)
        return humidity, temperature_f
