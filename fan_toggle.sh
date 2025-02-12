#!/usr/bin/bash

# Check if pigpiod is running, and start it if not
if ! pgrep -x "pigpiod" > /dev/null; then
    echo "pigpiod not running, starting it..."
    sudo pigpiod
    sleep 1  # Give it a moment to start
fi

# GPIO pin number
gpio_pin=18

# File to store the status
status_file="fan_status.txt"

# Function to read GPIO pin state
read_gpio_state() {
    gpio_state=$(pigs r $gpio_pin)
}

# Function to toggle GPIO pin state
toggle_gpio_state() {
    pigs w $gpio_pin $((1 - gpio_state))
    gpio_state=$(pigs r $gpio_pin)
}

# Function to write the new state to the status file
write_status_to_file() {
    echo $gpio_state > $status_file
}

# Read current GPIO pin state
read_gpio_state

# Toggle GPIO pin state
toggle_gpio_state

# Write the new state to the status file
#write_status_to_file

# Print the result (optional)
echo "Fan state toggled. New state: $gpio_state"

