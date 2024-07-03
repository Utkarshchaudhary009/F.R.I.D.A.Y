import json
from datetime import datetime
import os
import sys
import random
from DLG import *
# Get the parent directory of the current file
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# Add the parent directory to the Python path
sys.path.append(parent_dir)

from Brain.services.weather import get_weather
from BOS.Speak.playHT import playHT

# Placeholder for the imported function
def check_reminder():
    try:
        with open('../data/reminder.json', 'r+') as file:
            reminder_data = json.load(file)

            reminder_time = reminder_data.get('reminder_time')
            reminder_message = reminder_data.get('reminder_message')

            if reminder_time and reminder_message:
                reminder_datetime = datetime.strptime(reminder_time, '%Y-%m-%d %H:%M:%S')
                if reminder_datetime <= datetime.now():
                    return reminder_message

    except FileNotFoundError:
        print("No reminder found!")
    except json.JSONDecodeError:
        print("Reminder file is empty or corrupt!")
    
    return None

def get_time_of_day():
    current_hour = 22 #datetime.now().hour
    if 5 <= current_hour < 12:
        return "morning"
    elif 12 <= current_hour < 17:
        return "afternoon"
    elif 17 <= current_hour < 21:
        return "evening"
    else:
        return "night"

# Arrays of dynamic responses
morning_greetings = [
    "Good morning, ", "Have a happy morning, ", "Have a good morning, ", 
    "Rise and shine, ", "Top of the morning to you, ", "Good day to you, "
]
afternoon_greetings = [
    "Good afternoon, ", "Hope your afternoon is going well, ", 
    "Good day, ", "Enjoy your afternoon, ", "Hello, good afternoon, "
]
evening_greetings = [
    "Good evening, ", "Hope your evening is pleasant, ", 
    "Good to see you this evening, ", "Hello, good evening, ", "Evening, "
]
night_greetings = [
    "Hello, ", "Good night, ", "Hope you had a great day, ", 
    "Hi there, ", "Hello, good night, ", "Good to see you, "
]
weather_comments = [
    "The weather in {location} is currently {weather}. ", 
    "It's {weather} in {location} today. ", 
    "Currently, it's {weather} in {location}. ", 
    "The forecast for {location} is {weather}. ", 
    "Expect {weather} in {location}. "
]
happy_responses = [
    "You seem in a good mood today! ", "You're looking happy today! ", 
    "Great to see you happy! ", "You're in high spirits today! ", 
    "You have a bright smile today! "
]
sad_responses = [
    "I'm here if you need to talk. ", "It’s okay to feel sad sometimes. ", 
    "Let me know if I can help. ", "I’m here for you. ", 
    "Take your time, I’m here. "
]
stressed_responses = [
    "Take a deep breath, everything will be alright. ", 
    "Remember to relax and take it easy. ", 
    "Don't stress, things will work out. ", 
    "It's important to take breaks. ", 
    "Stay calm and carry on. "
]

def advanced_greeting(user_name, mood=None):
    greeting = ""

    # Time-based greetings
    time_of_day = get_time_of_day()
    if time_of_day == "morning":
        greeting += random.choice(morning_greetings)
    elif time_of_day == "afternoon":
        greeting += random.choice(afternoon_greetings)
    elif time_of_day == "evening":
        greeting += random.choice(evening_greetings)
    else:
        greeting += random.choice(night_greetings)

    # Personalization
    greeting += f"{user_name}. "

    # Context awareness
    weather_data = check_weather()
    if weather_data:
        location = weather_data["location"]
        weather = weather_data["weather"]
        greeting += random.choice(weather_comments).format(location=location, weather=weather)
    else:
        print("earr in providing weather")
    # # Emotion and sentiment
    # if mood == "happy":
    #     greeting += random.choice(happy_responses)
    # elif mood == "sad":
    #     greeting += random.choice(sad_responses)
    # elif mood == "stressed":
    #     greeting += random.choice(stressed_responses)

    # Dynamic content
    reminder_message = check_reminder()
    if reminder_message:
        greeting += f"Remember, {reminder_message}. "

    # Return the full greeting
    return greeting

# Check weather
def check_weather():
    try:
         print(get_weather())
         weather_data = get_weather()  # Assuming get_weather() returns a dictionary
         print(weather_data)
         if weather_data:
             data = weather_data.get('data')
             location = weather_data.get('location')
             if data:
                 weather_description = data.get('weather')
                 if weather_description:
                     description = weather_description[0].get('description')
                     return {"location": location, "weather": description}
                 else:
                     print("Failed to retrieve weather description.")
             else:
                 print("Failed to retrieve weather data.")
         else:
             print("Failed to retrieve weather information.")
             return None
    except:
        None
        
# Example usage
if __name__ == "__main__":
    while True:
        playHT(advanced_greeting("Utkarsh"))
        print(advanced_greeting("Utkarsh"))
