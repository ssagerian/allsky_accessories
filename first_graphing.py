import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class SensorData:
    def __init__(self):
        self.data_dict = {}
        self.data_dict['HS_TEMPERATURE'] = {'value': 0, 'expires': 600}
        self.data_dict['HS_HUMIDITY'] = {'value': 0, 'expires': 600}
        self.data_dict['HS_DEW_HEATER_STATUS'] = {'value': 'OFF', 'expires': 600}
        self.data_dict['HS_FAN_STATUS'] = {'value': 'OFF', 'expires': 600}

    def get_data_json(self):
        return json.dumps(self.data_dict, indent=2)

# Function to read temperature, humidity, dew heater status, and fan status
def read_sensor_data():
    # Replace the following lines with your actual sensor reading logic
    temperature = 25.0
    humidity = 50.0
    dew_heater_status = 'on'
    fan_status = 'off'

    return temperature, humidity, dew_heater_status, fan_status

# Function to update the data dictionary
def update_dict(data_dict, temperature, humidity, dew_heater_status, fan_status):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # home sky (HS) Update data dictionary
    data_dict['HS_TEMPERATURE'] = {'value': temperature, 'expires': 600}
    data_dict['HS_HUMIDITY'] = {'value': humidity, 'expires': 600}
    data_dict['HS_DEW_HEATER_STATUS'] = {'value': dew_heater_status, 'expires': 600}
    data_dict['HS_FAN_STATUS'] = {'value': fan_status, 'expires': 600}

    # Append temperature and humidity to the array
    data_dict['temperature_array'].append({'timestamp': timestamp, 'value': temperature})
    data_dict['humidity_array'].append({'timestamp': timestamp, 'value': humidity})

# Function to save the data dictionary as a JSON file
def save_to_json(data_dict, filename):
    with open(filename, 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)

# Function to plot temperature and humidity over time
def plot_data(data_dict):
    timestamps = [entry['timestamp'] for entry in data_dict['temperature_array']]
    temperatures = [entry['value'] for entry in data_dict['temperature_array']]
    humidities = [entry['value'] for entry in data_dict['humidity_array']]

    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Timestamp')
    ax1.set_ylabel('Temperature (°C)', color='tab:red')
    ax1.plot(timestamps, temperatures, color='tab:red')
    ax1.tick_params(axis='y', labelcolor='tab:red')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Humidity (%)', color='tab:blue')
    ax2.plot(timestamps, humidities, color='tab:blue')
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    fig.tight_layout()
    plt.title('Temperature and Humidity Over Time')
    plt.savefig('temperature_humidity_plot.png', transparent=True)
    #plt.show()

# Main function
def main():
    data_dict = {'temperature_array': [], 'humidity_array': []}
    data_json = {}
    while True:

        # Read sensor data
        temperature, humidity, dew_heater_status, fan_status = read_sensor_data()

        # Update data dictionary
        update_dict(data_dict, temperature, humidity, dew_heater_status, fan_status)
        update_json(data_dict, temperature, humidity, dew_heater_status, fan_status)

        # Save data dictionary to JSON file
        save_to_json(data_dict, 'sensor_data.json')

        # Plot temperature and humidity over time
        plot_data(data_dict)

        time.sleep(60)

if __name__ == "__main__":
    main()
