import subprocess

def set_monitor_mode(interface, channel):
    try:
        # Bring down the interface
        subprocess.run(['sudo', 'ifconfig', interface, 'down'], check=True)
        
        # Set the interface to monitor mode
        subprocess.run(['sudo', 'iwconfig', interface, 'mode', 'monitor'], check=True)
        
        # Bring up the interface
        subprocess.run(['sudo', 'ifconfig', interface, 'up'], check=True)
        
        # Set the interface to the specified channel
        subprocess.run(['sudo', 'iw', interface, 'set', 'channel', str(channel)], check=True)

        print(f"{interface} has been set to monitor mode on channel {channel}")
    
    except subprocess.CalledProcessError as e:
        print(f"Failed to set {interface} to monitor mode: {e}")

# Replace 'wlan1' with your actual interface and '60' with your desired channel
set_monitor_mode('wlan1', 60)