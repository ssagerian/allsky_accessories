import subprocess
import re

def get_cpu_statistics():
    command = "mpstat -P ALL 1 1"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode("utf-8")

def parse_cpu_statistics(output):
    # Split the output into lines
    lines = output.split('\n')

    # Initialize counters
    total_user = 0
    total_system = 0
    total_idle = 0

    # Iterate through lines starting from the third line (skipping header)
    for line in lines[3:]:
        # Extract values using regex
        values = re.findall(r'\d+\.\d+', line)
        if len(values) == 11:
            # Extract user, system, and idle times
            user, system, idle = map(float, values[1:4])
            
            # Add to total counters
            total_user += user
            total_system += system
            total_idle += idle

    return total_user, total_system, total_idle

if __name__ == "__main__":
    cpu_data = get_cpu_statistics()
    total_user, total_system, total_idle = parse_cpu_statistics(cpu_data)

    print(f"Total User Time Across All Cores: {total_user}%")
    print(f"Total System Time Across All Cores: {total_system}%")
    print(f"Total Idle Time Across All Cores: {total_idle}%")

