#!/bin/bash

# Check if a GPIO pin number is provided as a command-line argument
#if [ $# -eq 0 ]; then
#    echo "Usage: $0 <gpio_pin>"
#    exit 1
#fi

# GPIO pin number
gpio_pin=17

# File to store the status
status_file="dew_status.txt"

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
echo "Heater state toggled. New state: $gpio_state"

