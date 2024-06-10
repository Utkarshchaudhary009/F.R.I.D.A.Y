
def toggle_wifi(state):
    """
    Toggle Wi-Fi state.
    """
    # Your implementation to toggle Wi-Fi goes here
    print(f"Wi-Fi turned {state}")

def toggle_bluetooth(state):
    """
    Toggle Bluetooth state.
    """
    # Your implementation to toggle Bluetooth goes here
    print(f"Bluetooth turned {state}")

def toggle_battery_saver(state):
    """
    Toggle battery saver mode.
    """
    # Your implementation to toggle battery saver mode goes here
    print(f"Battery saver mode turned {state}")

def toggle_night_light(state):
    """
    Toggle night light mode.
    """
    # Your implementation to toggle night light mode goes here
    print(f"Night light mode turned {state}")

def toggle_flight_mode(state):
    """
    Toggle flight mode.
    """
    # Your implementation to toggle flight mode goes here
    print(f"Flight mode turned {state}")

def onoff(args):
    if args.thing == "wifi":
        toggle_wifi(args.action)
    elif args.thing == "bluetooth":
        toggle_bluetooth(args.action)
    elif args.thing == "battery_saver":
        toggle_battery_saver(args.action)
    elif args.thing == "night_light":
        toggle_night_light(args.action)
    elif args.thing == "flight_mode":
        toggle_flight_mode(args.action)

if __name__ == "__main__":
    onoff()
