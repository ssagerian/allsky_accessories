import time
import os
import atexit
import signal
from datetime import datetime, timedelta
import sys
import logging

if sys.platform.startswith('win'):
    # Windows-specific logging configuration
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
else:
    # Unix-like system logging configuration
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s', handlers=[logging.SysLogHandler()])

# Example log messages
#logging.info("This is an informational message.")
#logging.warning("This is a warning message.")
#logging.error("This is an error message.")


#directory_path = "/home/pi/allsky"
directory_path = "./"
data_to_save = [1, 2, 3, 4, 5]
data_lines = []
filename = datetime.now().strftime('%Y%m%d') + "_temperature_humidity_data.txt"
full_file_path: str = os.path.join(directory_path, filename)

def save_data():
    global full_file_path
    global data_lines
    # Save your data to a file or perform other actions
    logging.info("attempting to save data ")
    try:
        with open(full_file_path, "w") as file:
            file.write("\n".join(map(str, data_lines)))
    except Exception as e:
        logging.error(f"Error writing to file: {e}")


def handle_exit(signum, frame):
    global full_file_path
    logging.info(f"program exiting due to signal: {signum}")
    save_data()

def sleep_until_next_minute():
    current_time = datetime.now()
    next_minute = (current_time + timedelta(minutes=1)).replace(second=0, microsecond=0)
    # Calculate the number of seconds until the next whole minute
    sleep_seconds = (next_minute - current_time).total_seconds()
    # Sleep until the next whole minute
    time.sleep(sleep_seconds)

def main():
    global full_file_path
    global data_lines
    index = 0
    logging.info("main start up")
    #check to see if data exists
    try:
        if os.path.exists(full_file_path):
            # File exists, load data into list 'data'
            with open(full_file_path, 'r') as file:
                data_strs = file.readlines()
                data_lines = [int(line.strip()) for line in data_strs]
                index = data_lines[-1]
        else:
            data_lines = data_to_save
            index = data_lines[-1]

        while True:
            sleep_until_next_minute()
            index += 1
            data_lines.append(index)
            print("index ", index )
    except Exception as e:
        logging.warning(f"Main failed exception {e}.")

# start of execution
# Register the save_data function to be called at exit
atexit.register(save_data)
# Register the handle_exit function for specific signals
signal.signal(signal.SIGTERM, handle_exit)  # SIGTERM is the default signal sent by systemctl stop
signal.signal(signal.SIGINT, handle_exit)   # SIGINT is sent when you press Ctrl+C

if __name__ == "__main__":
    main()




