import screen_brightness_control as sbc
import os
import sys
# Ensure the parent directory is in sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    
def change_brightness(arguments):
    action = arguments.get("action")
    value = arguments.get("value","10")
    
    if '%' not in value:
        value = f'{value}%'
    
    current_brightness = sbc.get_brightness()[0]
    
    if value.endswith('%'):
        value = int(value[:-1])
    else:
        value = int(value)
    
    if action == "increase":
        new_brightness = min(current_brightness + value, 100)
    elif action == "decrease":
        new_brightness = max(current_brightness - value, 0)
    elif action == "adjust":
        new_brightness = min(value, 100)
    
    sbc.set_brightness(new_brightness)
    
    return {"response": f"Brightness set to {new_brightness}%."}
