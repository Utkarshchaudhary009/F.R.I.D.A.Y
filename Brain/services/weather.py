import requests
import sys
import os
from geocoder import ip
from datetime import datetime, timedelta

# Ensure the parent directory is in sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from Brain.utilities.readEnv import readEnv  # Absolute import

def get_weather(args):
    location=args.get("location",None)
    time=args.get("time",None)
    # OpenWeatherMap API key
    api_key = readEnv("WEATHER")
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    forecast_base_url = "http://api.openweathermap.org/data/2.5/forecast?"

    # If location is not provided, fetch the current location
    if not location:
        g = ip('me')
        location = g.city

    # Determine the date for the forecast
    today = datetime.today().date()
    if time is None or time.lower() == 'today':
        weather_date = today
    elif time.lower() == 'tomorrow':
        weather_date = today + timedelta(days=1)
    elif time.lower() == 'yesterday':
        weather_date = today - timedelta(days=1)
    else:
        weather_date = datetime.strptime(time, "%Y-%m-%d").date()

    # Construct final url
    complete_url = base_url + "q=" + location + "&appid=" + api_key + "&units=metric"
    forecast_url = forecast_base_url + "q=" + location + "&appid=" + api_key + "&units=metric"
    
    # Get response from the URL
    response = requests.get(complete_url)
    weather_data = response.json()

    if time and time.lower() != 'today':
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()

        # Filter forecast data for the specified date
        forecast_list = forecast_data.get('list', [])
        filtered_forecast = [item for item in forecast_list if datetime.utcfromtimestamp(item['dt']).date() == weather_date]

        if not filtered_forecast:
            return {"response": "No forecast data available for the specified date."}
        
        weather_data = filtered_forecast[0]

    # Check if the location is valid
    if weather_data["cod"] != "404":
        main = weather_data.get("main", {})
        wind = weather_data.get("wind", {})
        weather_desc = weather_data["weather"][0].get("description", "No description available")
        temperature = main.get("temp", "No data")
        feels_like = main.get("feels_like", "No data")
        pressure = main.get("pressure", "No data")
        humidity = main.get("humidity", "No data")
        wind_speed = wind.get("speed", "No data")
        visibility = weather_data.get("visibility", "No data")
        
        wind_deg = wind.get("deg", None)
        wind_directions = ["North", "North-Northeast", "Northeast", "East-Northeast", "East", "East-Southeast", "Southeast", "South-Southeast", "South", "South-Southwest", "Southwest", "West-Southwest", "West", "West-Northwest", "Northwest", "North-Northwest"]
        wind_direction = wind_directions[int((wind_deg / 22.5) + 0.5) % 16] if wind_deg is not None else "No data"
        
        weather_report = (
            f"The weather in {location} is {weather_desc}. The temperature is {temperature}°C, "
            f"feels like {feels_like}°C, wind speed is {wind_speed} meters per second from the {wind_direction}, "
            f"humidity is {humidity} percent,"
            f"and visibility is {visibility / 1000} Kilometer."
        )

        # Heatwave warning based on "feels like" temperature
        if feels_like != "No data" and feels_like >= 35:
            weather_report += " Warning: There is a heatwave."

    else:
        weather_report = "Location not found."
    
    return {"response": weather_report,"data":weather_data,"location":location}

# Example call
if __name__ == "__main__":
    print(get_weather())
