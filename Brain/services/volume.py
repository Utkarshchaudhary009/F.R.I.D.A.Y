from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pythoncom  # Import pythoncom
import sys

def change_volume(arguments):
    action = arguments.get("action")
    value = arguments.get("value")
    
    if '%' not in value:
        value = f'{value}%'

    # Initialize COM library
    pythoncom.CoInitialize()
    
    try:
        # Get the default audio device
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        
        # Get the current volume level
        current_volume = volume.GetMasterVolumeLevelScalar()
        
        if value.endswith('%'):
            value = float(value[:-1]) / 100.0
        else:
            value = float(value)
        
        if action == "increase":
            new_volume = min(current_volume + value, 1.0)
        elif action == "decrease":
            new_volume = max(current_volume - value, 0.0)
        elif action == "adjust":
            new_volume = min(value, 1.0)
        else:
            return {"response":"some error. Please specify the action."}
        # Set the new volume level
        volume.SetMasterVolumeLevelScalar(new_volume, None)
        
        return {"response": f"Volume set to {new_volume * 100:.2f}%."}
    finally:
        # Uninitialize COM library
        pythoncom.CoUninitialize()

if __name__ == "__main__":
    arguments = {"action": "adjust", "value": "100"}
    result = change_volume(arguments)
    print(result)
