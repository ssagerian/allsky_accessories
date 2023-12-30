import time
import syslog
import pigpio
from SensorData import SensorData
from si7020_I2C import si7020_I2C
import numpy as np
import matplotlib.pyplot as plt
import os
import signal
from datetime import datetime, timedelta
import atexit

# temperature and Humidity
TandH_data = []


def read_temperature_data_file():
    file_name = f"temperatureMonitor_data_{datetime.now().strftime('%Y-%m-%d')}.txt"

    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

        # Skip the header line
        lines = lines[1:]

        data_points = []
        for line in lines:
            values = line.strip().split(',')
            data_point = [float(val) if '.' in val else str(val) for val in values]
            data_points.append(data_point)

        return data_points

    except FileNotFoundError:
        print(f"The file '{file_name}' does not exist.")
        return []


def sleep_until_next_minute():
    current_time = datetime.now()
    next_minute = (current_time + timedelta(minutes=1)).replace(second=0, microsecond=0)

    # Calculate the number of seconds until the next whole minute
    sleep_seconds = (next_minute - current_time).total_seconds()

    # Sleep until the next whole minute
    time.sleep(sleep_seconds)


def plot_and_save_image(data):
    timestamps, humidities, temperatures = np.transpose(data)

    # Convert temperatures to numerical values
    temperatures = np.array(temperatures, dtype=float)

    # Convert timestamps to Python datetime objects
    timestamps = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in timestamps]

    fig, ax1 = plt.subplots(figsize=(10, 5), dpi=100)  # Set size to 8x5 inches at 100 dpi

    # Plot temperature on the left y-axis (ax1)
    color = 'tab:red'
    ax1.set_xlabel('Timestamp')
    ax1.set_ylabel('Temperature (F)', color=color)

    # Calculate uniform ticks for the temperature
    min_temp, max_temp = np.floor(min(temperatures)), np.ceil(max(temperatures))
    tick_interval = 10  # You can adjust this interval as needed
    temperature_ticks = np.arange(min_temp, max_temp + 1, tick_interval)

    ax1.plot(timestamps, temperatures, label='Temperature (F)', marker='o', color=color, alpha=0.5, zorder=1)
    ax1.set_yticks(temperature_ticks)
    ax1.tick_params(axis='y', labelcolor=color)

    # Create a second y-axis for humidity
    ax2 = ax1.twinx()

    # Convert humidity to integer values
    humidities = np.array([round(float(humidity)) for humidity in humidities], dtype=int)

    # Plot humidity on the right y-axis (ax2)
    color = 'tab:blue'
    ax2.set_ylabel('Humidity (%)', color=color)
    ax2.plot(timestamps, humidities, label='Humidity (%)', marker='o', color=color, alpha=0.5, zorder=2)
    ax2.tick_params(axis='y', labelcolor=color)

    # Format x-axis ticks to show only hours and minutes
    ax1.set_xticks(timestamps)
    ax1.set_xticklabels([dt.strftime('%H:%M') for dt in timestamps], rotation=45, ha='right')

    plot_path = '/home/pi/allsky/config/overlay/images/temp_humidity_plot.png'
    plt.title('Temperature and Humidity Over Time')
    plt.tight_layout()  # Adjust layout for better spacing
    plt.savefig(plot_path, transparent=True)
    plt.close()


def check_time(save_interval):
    timestamp = datetime.now()
    # Check if it's within the time window to save data
    target_time_start = datetime.strptime('11:40:00', '%H:%M:%S').time()
    target_time_end = (datetime.strptime('11:40:00', '%H:%M:%S') + timedelta(seconds=save_interval)).time()
    current_time = timestamp.time()
    if target_time_start <= current_time <= target_time_end:
        return True
    else:
        return False

def create_time_encoded_file_name(name):

    # Get the current date in the format 'YYYYMMDD'
    current_date = datetime.now().strftime('%Y%m%d')

    # Define the directory and filename format
    directory_format = "/home/pi/allsky/images/{}"
    filename_format = "{}" + name + ".txt"

    # Combine the directory and filename using the current date
    directory_path = directory_format.format(current_date)
    filename = filename_format.format(current_date)

    # Join the directory and filename to create the full file path
    full_file_path = os.path.join(directory_path, filename)
    return full_file_path


def save_data_to_file(data, filename):
    """ same temperature and humidty as a text file for future"""
    if os.path.exists(filename):
        # File exists, load data into list 'data'
        with open(filename, 'w') as file:
            # Write header
            file.write('Timestamp,Humidity (%),Temperature (F)\n')

            # Write data
            for data_point in data:
                formatted_data_point = [f'{val:.3f}' if isinstance(val, (float, float)) else str(val) for val in data_point]
                file.write(','.join(formatted_data_point) + '\n')
    else:
        file_not_found_file_name = f"temperatureMonitor_data_{datetime.now().strftime('%Y-%m-%d')}.txt"
        with open(file_not_found_file_name, 'w') as file:
            # Write header
            file.write('Timestamp,Humidity (%),Temperature (F)\n')
            # Write data
            for data_point in data:
                formatted_data_point = [f'{val:.3f}' if isinstance(val, (float, float)) else str(val) for val in data_point]
                file.write(','.join(formatted_data_point) + '\n')


def main():
    global TandH_data
    #syslog every 15 minutes
    report_time = (datetime.now() + timedelta(minutes=15)).replace(second=0, microsecond=0)
    # save at mid nite unitl I run this as a script from allsky
    save_time = datetime.now().replace(hour=0, second=0, minute=0, microsecond=0) + timedelta(days=1)

    # gpio controls
    pi = pigpio.pi()
    th_sensor = si7020_I2C()
    if not pi.connected:
        syslog.syslog(syslog.LOG_INFO, f"Unable to connect to pigpio daemon. Exiting.")
        exit()

    save_interval = 30  # Time window in seconds
    json_file_path = '/home/pi/allsky/config/overlay/extra/sensor_data.json'

    todays_name: str = ""

    # see if existing file is present and read it in or return empty list
    TandH_data = read_temperature_data_file()

    while True:
        # Call temperature and humidity functions
        humidity, temperature = th_sensor.get_humidity_and_temperatureF()
        # Round values to one significant digit
        temperature_rounded = round(temperature, 1)
        humidity_rounded = round(humidity, 1)

        # temp humidity and timestampe as its own data file
        time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_point = [time_stamp, humidity, temperature]
        TandH_data.append(data_point)

        # at midnight we start a new file
        if save_time < datetime.now():
            print(f"hello steve, save time:{save_time} time now:{datetime.now()}")
            save_data_to_file(TandH_data, todays_name)
            TandH_data = []
            save_time = datetime.now().replace(hour=0, second=0, minute=0, microsecond=0) + timedelta(days=1)
        else:
            # Create and save plot
            plot_and_save_image(TandH_data)
            todays_name = create_time_encoded_file_name("_temperature_humidity_data")

        # now check fan and heater status
        try:
            if 1 == pi.read(18):
                fan = "ON"
            else:
                fan = "OFF"
            if 1 == pi.read(17):
                heater = "ON"
            else:
                heater = "OFF"
        except pigpio.error as e:
            # Handle pigpio-specific exceptions
            syslog.syslog(syslog.LOG_INFO, f"Allsky pigpio An error occurred: {e}")
            exit()

        # now put in json format and save for overlay to use
        sensor_data = SensorData(temperature_rounded, humidity_rounded, heater, fan)
        sensor_data.data_dict["HS_TIME_STAMP"] = time_stamp
        # Update data dictionary
        sensor_data.save_to_json(json_file_path)

        if report_time < datetime.now():
            report_time = (datetime.now() + timedelta(minutes=15)).replace(second=0, microsecond=0)
            syslog.syslog(syslog.LOG_INFO, f"Allsky temperature: {temperature_rounded} F")

        # Sleep for a minute
        sleep_until_next_minute()

def shutdown_save( signal=None, stack_frame=None):
    todays_name = create_time_encoded_file_name("_temperature_humidity_data")
    save_data_to_file(TandH_data, todays_name)
    syslog.syslog(syslog.LOG_INFO, f"temperature monitor shutting down saving data to: {todays_name}")
    exit(0)


atexit.register(shutdown_save)
signal.signal(signal.SIGTERM, shutdown_save)  # SIGTERM is the default signal sent by systemctl stop
signal.signal(signal.SIGINT, shutdown_save)   # SIGINT is sent when you press Ctrl+C


if __name__ == "__main__":
    main()

