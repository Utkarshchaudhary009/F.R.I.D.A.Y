import screen_brightness_control as sbc

def change_brightness(arguments):
    action = arguments.get("action")
    value = arguments.get("value")
    
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
