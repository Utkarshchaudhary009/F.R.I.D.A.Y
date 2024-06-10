import subprocess

def manage_bluetooth(args):
    """
    Manage Bluetooth connections based on the provided action and device name.
    
    :param args: A dictionary with 'action' and 'device_name' keys
    """
    action = args.get("action", "").lower()
    device_name = args.get("device_name", "")

    if action == "connect":
        device_mac = name_to_mac(device_name)
        if device_mac:
            connect_to_bluetooth(device_mac)
        else:
            print(f"Device '{device_name}' not found.")
    elif action == "forget":
        device_mac = name_to_mac(device_name)
        if device_mac:
            forget_bluetooth(device_mac)
        else:
            print(f"Device '{device_name}' not found.")
    elif action == "list":
        list_available_bluetooth_devices()
    else:
        print(f"Unknown action: {action}")

def connect_to_bluetooth(device_mac):
    """
    Connect to a Bluetooth device using the provided MAC address.
    
    :param device_mac: The MAC address of the Bluetooth device
    """
    try:
        subprocess.run(["bluetoothctl", "power", "on"], check=True)
        subprocess.run(["bluetoothctl", "agent", "on"], check=True)
        subprocess.run(["bluetoothctl", "default-agent"], check=True)
        subprocess.run(["bluetoothctl", "connect", device_mac], check=True)
        print(f"Successfully connected to {device_mac}")
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to connect to {device_mac}: {e}")

def forget_bluetooth(device_mac):
    """
    Forget a Bluetooth device using the provided MAC address.
    
    :param device_mac: The MAC address of the Bluetooth device
    """
    try:
        subprocess.run(["bluetoothctl", "remove", device_mac], check=True)
        print(f"Successfully forgot {device_mac}")
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to forget {device_mac}: {e}")

def list_available_bluetooth_devices():
    """
    List all available Bluetooth devices.
    """
    try:
        result = subprocess.run(["bluetoothctl", "scan", "on"], capture_output=True, text=True, check=True, timeout=10)
        lines = result.stdout.splitlines()
        
        available_devices = {}
        for line in lines:
            if "Device" in line:
                parts = line.split()
                if len(parts) >= 3:
                    device_mac = parts[1]
                    device_name = ' '.join(parts[2:])
                    available_devices[device_name] = device_mac
        
        print("Available Bluetooth devices:")
        for device_name, device_mac in available_devices.items():
            print(f"{device_name}: {device_mac}")
        
        return available_devices
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to list available Bluetooth devices: {e}")
    except subprocess.TimeoutExpired:
        print("Bluetooth scan timed out.")
    return {}

def name_to_mac(device_name):
    """
    Get the MAC address of a Bluetooth device by its name.
    
    :param device_name: The name of the Bluetooth device
    :return: The MAC address of the device, or None if not found
    """
    available_devices = list_available_bluetooth_devices()
    return available_devices.get(device_name)

# Example usage
manage_bluetooth({"action": "connect", "device_name": "jarvis"})
manage_bluetooth({"action": "forget", "device_name": "jarvis"})
manage_bluetooth({"action": "list"})
