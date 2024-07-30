import subprocess
import time

# Define the wireless interface
INTERFACE = "wlan1"

# Function to execute system commands
def run_command(command):
    subprocess.call(command, shell=True)

# Start monitor mode on the specified interface
def start_monitor_mode(interface):
    run_command(f"ifconfig {interface} down")
    run_command(f"iwconfig {interface} mode monitor")
    run_command(f"ifconfig {interface} up")

# Hop to the given channel
def hop_to_channel(interface, channel):
    run_command(f"iwconfig {interface} channel {channel}")
    print(channel)

# Main function to perform channel hopping
def channel_hopper(interface, channels, dwell_time=10):
    #start_monitor_mode(interface)
    try:
        while True:
            for channel in channels:
                hop_to_channel(interface, channel)
                time.sleep(dwell_time)
    except KeyboardInterrupt:
        print("\nStopped channel hopping")

# Define an array of channels you want to hop between
CHANNELS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 149, 153, 157, 161]

# Run the channel hopper
channel_hopper(INTERFACE, CHANNELS)
