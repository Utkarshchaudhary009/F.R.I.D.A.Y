import psutil
import requests
import pyttsx3
import time
import sys
import os

# Get the parent directory of the current file (Moniter_System.py)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# Add the parent directory to the Python path
sys.path.append(parent_dir)

from Brain.services.weather import get_weather
from speak import speak

# Check RAM usage
def check_ram():
    ram = psutil.virtual_memory()
    if ram.percent > 95:
        speak("Warning: Your RAM usage is above 95%. Consider closing some applications.")

# Check battery status
def check_battery():
    battery = psutil.sensors_battery()
    if battery.percent < 20 and not battery.power_plugged:
        speak("Your battery is below 20%. Please plug in your charger.")
    elif battery.percent == 99.50 and battery.power_plugged:
        speak("Your battery is fully charged. You might want to unplug your charger.")

# Check storage space
def check_storage():
    disk = psutil.disk_usage('/')
    if disk.percent > 90:
        speak("Warning: Your storage usage is above 90%. Consider cleaning up some space.")

# Check internet connectivity
def check_internet():
    try:
        requests.get('https://www.google.com/', timeout=5)
    except requests.ConnectionError:
        speak("You are not connected to the internet. Please check your connection.")
    except:
        pass

# Check weather
def check_weather():
    weather_data = get_weather()  # Assuming get_weather() returns a dictionary
    if weather_data:
        data = weather_data.get('data')
        location = weather_data.get('location')
        if data:
            weather_description = data.get('weather')
            if weather_description:
                description = weather_description[0].get('description')
                main = data.get("main", {})
                temperature = main.get("temp", "No data")
                if temperature > 40 :
                    speak(f"The current weather in {location} is {description}, with a temperature of {temperature} degrees Celsius.")
            else:
                print("Failed to retrieve weather description.")
        else:
            print("Failed to retrieve weather data.")
    else:
        print("Failed to retrieve weather information.")

# Main loop to check all metrics
def monitor_system():
    while True:
        check_ram()
        check_battery()
        check_storage()
        check_internet()
        #check_weather()
        #time.sleep(3600)  # Check every hour

if __name__ == "__main__":
    
    monitor_system()
