import smbus
import json
import logging

class I2CDeviceManager:
    def __init__(self, bus_number=1, log_level=logging.INFO):
        self.bus = smbus.SMBus(bus_number)
        self.logger = self.setup_logger(log_level)

    def setup_logger(self, log_level):
        logger = logging.getLogger("I2CDeviceManager")
        logger.setLevel(log_level)
        # Configure your desired logging format and handlers here
        return logger

    def write_register(self, address, register, value):
        self.bus.write_byte_data(address, register, value)
        self.logger.info(f"Write to device at address {hex(address)}, register {hex(register)}: {hex(value)}")

    def read_register(self, address, register):
        value = self.bus.read_byte_data(address, register)
        self.logger.info(f"Read from device at address {hex(address)}, register {hex(register)}: {hex(value)}")
        return value

    def to_json(self, data):
        return json.dumps(data)

class Device1:
    def __init__(self, manager, address):
        self.manager = manager
        self.address = address

    def set_gain(self, high_gain=True):
        value = 0x10 if high_gain else 0x00
        self.manager.write_register(self.address, 0x01, value)

    def start_integration_cycle(self):
        self.manager.write_register(self.address, 0x02, 0x08)

class DeviceSI7021:
    def __init__(self, manager, address=0x40):
        self.manager = manager
        self.address = address
        heater_map = {0: "OFF", 1: "ON"}
        vdd_map = {0: "OK", 1: "LOW!"}
        resolution_mapping = {
       	    (0, 0): "RH: 12 bit, Temp: 14 bit",
            (0, 1): "RH: 8 bit, Temp: 12 bit",
            (1, 0): "RH: 10 bit, Temp: 13 bit",
            (1, 1): "RH: 11 bit, Temp: 11 bit",
        }
        try:
            self.address = address
            self.temperatureCmd = TEMPERATURE_COMMAND
            self.humidityCmd = HUMIDITY_COMMAND
            try:
                # init chip
                self.manager.write_byte(self.address, 0xFE)  # reset sensor
                time.sleep(1)
                self.manager.write_byte_data(self.address, 0xE6, 0x04)  # heater on Temp Resolution == 12 bits, RH= 8 bits
                time.sleep(1)
                read_data = self.manager.read_byte_data(self.address, 0xE7)  # read register 1
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
        temp = self.manager.read_word_data(self.address, 0xE0)  # read temp from last humidity conversion
        temp = ((0x00FF & temp) << 8) + ((0xFF00 & temp) >> 8)
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
        humd = self.manager.read_word_data(self.address, 0xE5)
        humd = ((0x00FF & humd) << 8) + ((0xFF00 & humd) >> 8)
        humidity = ((125 * humd) / 65536) - 6
        return humidity

    def get_humidity_and_temperatureF(self):  # Call temperature and humidity functions
        humidity = self.get_humidity()
        temperature = self.get_temperature()
        temperature_f = si7020_I2C.celsius_to_fahrenheit(temperature)
        return humidity, temperature_f

# Example usage:
manager = I2CDeviceManager()
si7021 = DeviceSI7021(manager)
device1 = Device1(manager, address=0x20)

device1.set_gain(high_gain=True)
device1.start_integration_cycle()

#sensor_data = device2.read_sensor_data()
#print(f"Sensor data from Device2: {sensor_data}")
