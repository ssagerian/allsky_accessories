import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time
from datetime import datetime, timedelta

def get_humidity_and_temperatureF():
    humidity = np.random.uniform(20, 90)
    temperature = np.random.uniform(60, 80)
    return humidity, temperature

def save_data_to_file(data, filename):
    with open(filename, 'w') as file:
        # Write header
        file.write('Timestamp,Humidity (%),Temperature (F)\n')

        # Write data
        for data_point in data:
            formatted_data_point = [f'{val:.3f}' if isinstance(val, (float, float)) else str(val) for val in data_point]
            file.write(','.join(formatted_data_point) + '\n')

# ...

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

# ...

# ...

import time

# ...

def main():
    data = []
    save_interval = 120  # Time window in seconds (2 minutes)

    while True:
        humidity, temperature = get_humidity_and_temperatureF()
        timestamp = datetime.now()

        data_point = [timestamp.strftime('%Y-%m-%d %H:%M:%S'), humidity, temperature]
        data.append(data_point)

        print(f'Time: {timestamp.strftime("%Y-%m-%d %H:%M:%S")}, Humidity: {humidity}%, Temperature: {temperature:.2f}°F')

        time.sleep(5)  # Reduced sleep time for testing

        # Check if it's within the time window to save data
        target_time_start = datetime.strptime('12:59:00', '%H:%M:%S').time()
        target_time_end = (datetime.strptime('12:59:00', '%H:%M:%S') +
                           timedelta(seconds=save_interval)).time()

        current_time = timestamp.time()
        if target_time_start <= current_time <= target_time_end:
            save_data_to_file(data, 'temp_humidity_data.dat')
            print('Data saved to temp_humidity_data.dat')

            # Clear data for the new day
            data = []
            # Wait until the time window is over
            time.sleep(save_interval)
        else:
            # Create and save plot
            plot_and_save_data(data)
            print('Plot saved to temp_humidity_plot.png')

# ...

# ...

if __name__ == "__main__":
    main()
