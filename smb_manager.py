import smbus
import struct
import json
import logging

class I2CDeviceManager:
    """ the device manager creates an instance of the smb bus and lets device drivers use it for data requests

    ToDo:  put each bus access in a try block to catch errors related to device missing dead or whatever
    """
    def __init__(self, bus_number=1, log_level=logging.INFO, allow_logging=true):
        self.ok_2_log = allow_logging
        self.bus = smbus.SMBus(bus_number)
        self.logger = self.setup_logger(log_level)

    def m_logging_off(self):
        self.ok_2_log = False

    def m_logging_on(self):
        self.ok_2_log = True

    def m_setup_logger(self, log_level):
        logger = logging.getLogger("I2CDeviceManager")
        logger.setLevel(log_level)
        # Configure your desired logging format and handlers here
        return logger

    def m_write_byte(self, address,  value):
        """ master over ride of write byte """
        self.bus.write_byte(address,  value)
        if self.ok_2_log:
            self.logger.info(f"Write byte to device at address {hex(address)}, value : {hex(value)}")

    def m_read_byte(self, address, register):
        """ master override of smb bus read byte """
        value = self.bus.read_byte(address, register)
        if self.ok_2_log:
            self.logger.info(f"Read byte from device at address {hex(address)}, value : {hex(value)}")
        return value

    def m_read_byte_data(self, address, register):
        """ master override of smb bus read byte data """
        value = self.bus.read_byte_data(address, register)
        if self.ok_2_log:
            self.logger.info(f"Read byte data from device at address {hex(address)}, register {hex(register)}: {hex(value)}")
        return value

    def m_write_byte_data(self, address, register, value):
        """ master override of smb bus write byte data """
        self.bus.write_byte_data(address, register, value)
        if self.ok_2_log:
            self.logger.info(f"Read byte data from device at address {hex(address)}, register {hex(register)}: {hex(value)}")
        return value


    def m_write_word_data(self, address, register, value):
        """ master override of smb bus write WORD data """
        # Check if the value is a 2-byte word
        if not isinstance(value, int) or not struct.calcsize('H') == 2:
            raise ValueError("The 'value' must be a 2-byte word.")
        # Ensure that the value is within the 16-bit range (0 to 65535)
        if not 0 <= value <= 0xFFFF:
            raise ValueError("The 'value' must be a 16-bit unsigned integer.")
        self.bus.write_word_data(address, register, value)
        if self.ok_2_log:
            self.logger.info(f"Write word data from device at address {hex(address)}, register {hex(register)}: {hex(value)}")


    def m_read_word_data(self, address, register):
        """ master override of smb bus read WORD data """
        value = self.bus.read_word_data(address, register)
        if self.ok_2_log:
            self.logger.info(f"Read word data from device at address {hex(address)}, register {hex(register)}: {hex(value)}")
        return value

    def m_write_block_data(self, address, register, block):
        """ master override of smb bus write block list data """
        if not isinstance(block, list):
            raise ValueError("The 'block' must be a list")
        # Ensure that the value is within the 16-bit range (0 to 65535)
        self.bus.write_block_data(address, register, block)
        if self.ok_2_log:
            self.logger.info(f"Write word data from device at address {hex(address)}, register {hex(register)}: {block}")


    def m_read_block_data(self, address, register):
        """ master override of smb bus read WORD data """
        value = self.bus.read_block_data(address, register)
        if self.ok_2_log:
            self.logger.info(f"Read word data from device at address {hex(address)}, register {hex(register)}: {hex(value)}")
        return value

    def to_json(self, data):
        return json.dumps(data)

class PhotoDiode:
    def __init__(self):
        # Initialize attributes
        self.last_read = 0
        self.ave_value = 0
        self.upper_threshold = 0
        self.lower_threshold = 0
        self.read_count = 0
        self.cumulative_sum = 0

    def set(self,value ):
        self.last_read = value
        # Update count and cumulative sum
        self.read_count += 1
        self.cumulative_sum += self.last_read
        if self.read_count > 0:
            self.ave_value = self.cumulative_sum / self.read_count


class DeviceTSL2560:
    """
    control register defs
    """
    CONTROL_ADR = 0x00
    TIMING_ADR = 0x01
    THRESHOLD_LOW_LSB_ADR = 0x02
    THRESHOLD_LOW_MSB_ADR = 0x03
    THRESHOLD_HIGH_LSB_ADR = 0x04
    THRESHOLD_HIGH_MSB_ADR = 0x05
    INTERUPT_ADR = 0x06
    CRC_ADR = 0x08
    ID_ADR = 0x0A
    CHANNEL0_LSB_ADR = 0x0C
    CHANNEL0_MSB_ADR = 0x0D
    CHANNEL1_LSB_ADR = 0x0E
    CHANNEL1_MSB_ADR = 0x0F

    """ command register values"""
    COMMAND = 0b10000000 #
    COMMAND_CLEAR_ISR  =   0b01000000
    COMMAND_IS_WORD_OP  =  0b00100000
    COMMAND_IS_BLOCK_OP =  0b00010000

    """ command register values"""
    CONTROL_POWER_ON = 0x03

    """ command register values"""
    CONTROL_POWER_ON = 0x03

    """ Timing register values"""
    TIMING_GAIN_16X = 0x10
    TIMING_MANUAL_START = 0x0B
    TIMING_MANUAL_STOP  = 0x03
    TIMING_INTEGRATION_13ms  = 0x00
    TIMING_INTEGRATION_101ms = 0x01
    TIMING_INTEGRATION_MANUAL = 0x03

    """ Interrupt Threshold register values"""
    INTERRUPT_DISABLE  = 0b00000000
    INTERRUPT_LEVEL     = 0b00010000
    INTERRUPT_SMB_ALERT = 0b00100000
    INTERRUPT_SMB_TEST  = 0b00100000 # same as alert
    INTERRUPT_PERSIST_EVERY_CYCLE = 0x00
    INTERRUPT_PERSIST_ANY_CYCLE   = 0x01 #Any value outside of threshold range
    INTERRUPT_PERSIST_2_CYCLES    = 0x02 # 2x integration time periods out of range
    INTERRUPT_PERSIST_3_CYCLES    = 0x03
    INTERRUPT_PERSIST_4_CYCLES    = 0x04
    INTERRUPT_PERSIST_5_CYCLES    = 0x05
    INTERRUPT_PERSIST_6_CYCLES    = 0x06
    INTERRUPT_PERSIST_7_CYCLES    = 0x07
    INTERRUPT_PERSIST_8_CYCLES    = 0x08
    INTERRUPT_PERSIST_9_CYCLES    = 0x09
    INTERRUPT_PERSIST_10_CYCLES   = 0x0A
    INTERRUPT_PERSIST_11_CYCLES   = 0x0B
    INTERRUPT_PERSIST_12_CYCLES   = 0x0C
    INTERRUPT_PERSIST_13_CYCLES   = 0x0D
    INTERRUPT_PERSIST_14_CYCLES   = 0x0E
    INTERRUPT_PERSIST_15_CYCLES   = 0x0F # 15x integration time periods out of range

    """ Id and version register values"""
    ID_PART_NUMBER_BITS     = 0xF0
    ID_VERSION_NUMBER_BITS  = 0x0F
    id_parts_map = {0: " TSL2560", 0x10: " TSL2561", 0xF0: "unknown"}

    """ channel defs"""
    CHANNEL_0 = 0
    CHANNEL_1 = 1

    def __init__(self, manager, address=0x39, log=true):
        self.manager = manager
        self.address = address
        self.channel0 = PhotoDiode()
        self.channel1 = PhotoDiode()
        self.id = 0xFF
        self.command = 0
        try:
            # power on
            self.command |= self.COMMAND
            self.command |= self.CONTROL_ADR
            data = self.CONTROL_POWER_ON
            self.manager.m_write_byte_data(self.address, self.command, data)
            time.sleep(0.2)
            # read id
            self.command = 0
            self.command |= self.COMMAND
            self.command |= self.ID_ADR
            self.id = self.manager.m_read_byte_data(self.address, self.command)
            id_str = f"{id_parts_map.get(self.id & 0xF0 )} version {self.id_parts_map.get(0x0F & self.id)}"
            self.manager.logger.info(id_str)
        except IOError as e:
            print(f" Failed to initialize TSL2560-I2C device: {e}")
            exit(1)

    def get_channel(self, channel_number):
        self.command = 0
        self.command |= self.COMMAND
        self.command |= self.COMMAND_IS_WORD_OP
        if channel_number == self.CHANNEL_0:
            self.command |= self.CHANNEL0_LSB_ADR
            value = self.manager.m_read_word_data(self.address, self.command)
            channel0.set(value)
        else:
            self.command |= self.CHANNEL1_LSB_ADR
            value = self.manager.m_read_word_data(self.address, self.command)
            channel1.set(value)
        return channel_number, value

    def get_channel_average(self, channel_number):
        if channel_number == self.channel0:
            return self.channel0.ave_value
        if channel_number == self.channel1:
            return self.channel1.ave_value
        else:
            raise ValueError(f"channel number out of range {channel_number}.")

    def get_channel_0_lux(self):
        pass

    def isr_callback(self):
        pass

    def set_gain(self, high_gain=True):
        pass

    def start_integration_cycle(self):
        pass

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
