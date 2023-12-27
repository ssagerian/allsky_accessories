#!/bin/bash

# Source directory (where the YYYYMMDD directories are located)
source_directory="/home/pi/allsky/images"

# Destination directory on the remote server
destination_directory="pi@10.0.0.35:/mnt/homesky_ftp/images/"

# Log file
log_file="/var/log/allsky.log"

# Find directories that are two days old or older
cd "$source_directory" 
find_result=$(find . -maxdepth 1 -type d -ctime +1)

# Check if any directories were found
if [ -z "$find_result" ]; then
    echo "No directories found matching the criteria."
    logger -p local0.info "No directories found matching transfer criteria: $dirpath"
    exit 0
fi

# Iterate over the found directories
while IFS= read -r dirpath; do
    # Extract the directory name (YYYYMMDD format)
    dir_name=$(basename "$dirpath")

    # Use scp to transfer the contents of the directory to the remote server
    scp -r "$dirpath" "$destination_directory$dir_name"
    
    # Check the exit status of the scp command
    if [ $? -ne 0 ]; then
       logger -p local0.info "Transfer Failed $destination_directory$dir_name"
       exit 1  # Exit with a non-zero status to indicate failure
    fi

    # Optional: Remove the local directory after transfer
    rm -rf "$dirpath"

    # Log success
    logger -p local0.info "Transfer successful for directory: $dirpath"
    echo "Transfer successful for directory: $dirpath" >> "$log_file"

    # Print success
    echo "Transfer successful for directory: $dirpath"
done <<< "$find_result"

