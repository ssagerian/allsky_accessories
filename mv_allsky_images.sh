#!/bin/bash

# Source directory (where the YYYYMMDD directories are located)
source_directory="/home/pi/allsky/images"

# Destination directory on the remote server
destination_directory="pi@10.0.0.35:/mnt/homesky_ftp/images/"

# Log file
log_file="/var/log/allsky.log"

# Find directories that are two days old or older
find_result=$(find "$source_directory" -maxdepth 1 -type d -ctime +1)

# Check if any directories were found
if [ -z "$find_result" ]; then
    echo "No directories found matching the criteria."
    exit 0
fi

# Iterate over the found directories
while IFS= read -r dirpath; do
    # Extract the directory name (YYYYMMDD format)
    dir_name=$(basename "$dirpath")

    # Use scp to transfer the contents of the directory to the remote server
    scp -r "$dirpath" "$destination_directory$dir_name"

    # Optional: Remove the local directory after transfer
    # rm -r "$dirpath"

    # Log success
    logger -p local0.info "Transfer successful for directory: $dirpath"
    echo "Transfer successful for directory: $dirpath" >> "$log_file"

    # Print success
    echo "Transfer successful for directory: $dirpath"
done <<< "$find_result"

