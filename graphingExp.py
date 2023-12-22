import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time
from datetime import datetime

def get_humidity_and_temperatureF():
    humidity = np.random.uniform(20, 90)
    temperature = np.random.uniform(60, 80)
    return humidity, temperature

def save_data_to_file(data, filename):
    np.savetxt(filename, data, delimiter=',', fmt='%.2f', header='Humidity (%), Temperature (F)', comments='')

# ...

def plot_and_save_data(data):
    timestamps, humidities, temperatures = np.transpose(data)

    # Convert temperatures to numerical values
    temperatures = np.array(temperatures, dtype=float)

    # Convert timestamps to Python datetime objects
    timestamps = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in timestamps]

    fig, ax1 = plt.subplots(figsize=(12, 8))  # Create a figure with a single axes

    # Plot temperature on the left y-axis (ax1)
    color = 'tab:red'
    ax1.set_xlabel('Timestamp')
    ax1.set_ylabel('Temperature (F)', color=color)

    # Calculate uniform ticks for the temperature
    min_temp, max_temp = np.floor(min(temperatures)), np.ceil(max(temperatures))
    tick_interval = 10  # You can adjust this interval as needed
    temperature_ticks = np.arange(min_temp, max_temp + 1, tick_interval)

    ax1.plot(timestamps, temperatures, label='Temperature (F)', marker='o', color=color)
    ax1.set_yticks(temperature_ticks)
    ax1.tick_params(axis='y', labelcolor=color)

    # Create a second y-axis for humidity
    ax2 = ax1.twinx()

    # Convert humidity to integer values
    humidities = np.array([round(float(humidity)) for humidity in humidities], dtype=int)

    # Plot humidity on the right y-axis (ax2)
    color = 'tab:blue'
    ax2.set_ylabel('Humidity (%)', color=color)
    ax2.plot(timestamps, humidities, label='Humidity (%)', marker='o', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # Format x-axis ticks to show only hours and minutes
    ax1.set_xticks(timestamps)
    ax1.set_xticklabels([dt.strftime('%H:%M') for dt in timestamps], rotation=45, ha='right')

    plt.title('Temperature and Humidity Over Time')
    plt.tight_layout()  # Adjust layout for better spacing
    plt.savefig('temp_humidity_plot.png', transparent=True)
    plt.close()

# ...

def main():
    data = []

    while True:
        humidity, temperature = get_humidity_and_temperatureF()
        timestamp = datetime.now()

        data_point = [timestamp.strftime('%Y-%m-%d %H:%M:%S'), humidity, temperature]
        data.append(data_point)

        print(f'Time: {timestamp.strftime("%Y-%m-%d %H:%M:%S")}, Humidity: {humidity}%, Temperature: {temperature:.2f}°F')

        time.sleep(2)  # Reduced sleep time for testing

        # Check if it's a new day to save data
        if timestamp.strftime('%H:%M:%S') == '00:00:00':
            save_data_to_file(data, 'temp_humidity_data.dat')
            print('Data saved to temp_humidity_data.dat')

            # Clear data for the new day
            data = []

        # Create and save plot
        plot_and_save_data(data)
        print('Plot saved to temp_humidity_plot.png')

if __name__ == "__main__":
    main()
