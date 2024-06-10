import subprocess

def WiFi(args):
    """
    Manage Wi-Fi connections based on the provided action.
    
    :param args: An object with 'action', 'ssid', and 'password' attributes
    """
    action = args.action.lower()
    
    if action == "connect":
        connect_to_wifi(args)
    elif action == "forget":
        forget_wifi(args)
    elif action == "list":
        list_available_wifis()
    else:
        print(f"Unknown action: {action}")

def connect_to_wifi(args):
    """
    Connect to a Wi-Fi network using the provided arguments.
    
    :param args: An object with 'ssid' and 'password' attributes
    """
    ssid = args.ssid
    password = args.password

    try:
        # Create a network configuration for WPA/WPA2
        config = f"""
        network={{
            ssid="{ssid}"
            psk="{password}"
        }}
        """
        # Write the configuration to a temporary file
        with open("/tmp/wpa_supplicant.conf", "w") as config_file:
            config_file.write(config)
        
        # Kill any existing wpa_supplicant instances
        subprocess.run(["sudo", "killall", "wpa_supplicant"], check=True)
        
        # Connect using the wpa_supplicant configuration file
        subprocess.run(["sudo", "wpa_supplicant", "-B", "-i", "wlan0", "-c", "/tmp/wpa_supplicant.conf"], check=True)
        
        # Obtain an IP address via DHCP
        subprocess.run(["sudo", "dhclient", "wlan0"], check=True)
        
        print(f"Successfully connected to {ssid}")
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to connect to {ssid}: {e}")

def forget_wifi(args):
    """
    Forget a Wi-Fi network using the provided arguments.
    
    :param args: An object with 'ssid' attribute
    """
    ssid = args.ssid

    try:
        # List all saved networks
        result = subprocess.run(["sudo", "wpa_cli", "list_networks"], capture_output=True, text=True, check=True)
        networks = result.stdout.splitlines()

        # Find the network ID corresponding to the given SSID
        network_id = None
        for network in networks:
            if ssid in network:
                network_id = network.split()[0]
                break

        if network_id is not None:
            # Remove the network from wpa_supplicant
            subprocess.run(["sudo", "wpa_cli", "remove_network", network_id], check=True)
            subprocess.run(["sudo", "wpa_cli", "save_config"], check=True)
            print(f"Successfully forgot {ssid}")
        else:
            print(f"No network found with SSID {ssid}")
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to forget {ssid}: {e}")

def list_available_wifis():
    """
    List all available Wi-Fi networks.
    """
    try:
        # Scan for available networks
        subprocess.run(["sudo", "iwlist", "wlan0", "scan"], check=True)
        
        # Get the scan results
        result = subprocess.run(["sudo", "iwlist", "wlan0", "scan"], capture_output=True, text=True, check=True)
        networks = result.stdout.splitlines()
        
        available_networks = []
        for line in networks:
            if "ESSID" in line:
                ssid = line.split(":")[1].strip().strip('"')
                available_networks.append(ssid)
        
        print("Available Wi-Fi networks:")
        for network in available_networks:
            print(network)
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to list available Wi-Fi networks: {e}")



# Connect to a Wi-Fi network
WiFi({"action":"connect", "ssid":"realme 8i", "password":"your_password_here"})

# Forget a Wi-Fi network
WiFi({"action":"forget", "ssid":"realme 8i"})

# List available Wi-Fi networks
WiFi({"action":"list"})
