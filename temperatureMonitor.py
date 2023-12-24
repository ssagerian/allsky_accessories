import time
import syslog
import pigpio
from SensorData import SensorData
from si7020_I2C import si7020_I2C
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta

def sleep_until_next_minute():
    current_time = datetime.now()
    next_minute = (current_time + timedelta(minutes=1)).replace(second=0, microsecond=0)

    # Calculate the number of seconds until the next whole minute
    sleep_seconds = (next_minute - current_time).total_seconds()

    # Sleep until the next whole minute
    time.sleep(sleep_seconds)


def plot_and_save_data(data):
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

    plt.title('Temperature and Humidity Over Time')
    plt.tight_layout()  # Adjust layout for better spacing
    plt.savefig('temp_humidity_plot.png', transparent=True)
    plt.close()


def check_time(save_interval):
    timestamp = datetime.now()
    # Check if it's within the time window to save data
    target_time_start = datetime.strptime('02:00:00', '%H:%M:%S').time()
    target_time_end = (datetime.strptime('02:00:00', '%H:%M:%S') + timedelta(seconds=save_interval)).time()
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
    filename_format = "{}"+ name+ ".txt"

    # Combine the directory and filename using the current date
    directory_path = directory_format.format(current_date)
    filename = filename_format.format(current_date)

    # Join the directory and filename to create the full file path
    full_file_path = os.path.join(directory_path, filename)
    return full_file_path


def save_data_to_file(data, filename):
    """ same temperature and humidty as a text file for future"""
    with open(filename, 'w') as file:
        # Write header
        file.write('Timestamp,Humidity (%),Temperature (F)\n')

        # Write data
        for data_point in data:
            formatted_data_point = [f'{val:.3f}' if isinstance(val, (float, float)) else str(val) for val in data_point]
            file.write(','.join(formatted_data_point) + '\n')


def main():
    pi = pigpio.pi()
    th_sensor = si7020_I2C()
    if not pi.connected:
        syslog.syslog(syslog.LOG_INFO, f"Unable to connect to pigpio daemon. Exiting.")
        exit()

    save_interval = 30  # Time window in seconds
    json_file_path = '/home/ssagerian/allsky/config/overlay/extra/sensor_data.json'
    data = []
    todays_name: str = ""

    while True:
        # Call temperature and humidity functions
        humidity, temperature = th_sensor.get_humidity_and_temperatureF()
        timestamp = datetime.now()
        print(" time is ", timestamp.strftime('%Y-%m-%d %H:%M:%S'))
        # Round values to one significant digit
        temperature_rounded = round(temperature, 1)
        humidity_rounded = round(humidity, 1)

        # temp humidity and timestampe as its own data file
        data_point = [timestamp.strftime('%Y-%m-%d %H:%M:%S'), humidity, temperature]
        data.append(data_point)

	# at midnight we start a new file
        if check_time(save_interval):
            save_data_to_file(data, todays_name)
            # Clear data for the new day
            data = []
        else:
            # Create and save plot
            print("saving data")
            plot_and_save_data(data)
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
        sensor_data.data_dict["HS_TIME_STAMP"] = timestamp
        # Update data dictionary
        sensor_data.save_to_json(json_file_path)

        syslog.syslog(syslog.LOG_INFO, f"Allsky Temperature: {temperature_rounded} F")

        # Sleep for a minute
        sleep_until_next_minute()

if __name__ == "__main__":
    main()

