import os
import json
from datetime import datetime, timedelta
import requests
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
# from app.main import BASE_DIR # Fix circular import later
from app.config import get_openweathermap_api_key


# weather_json_file = BASE_DIR / "data" / "weather_forecast.json" # Fix circular import later
weather_json_file = Path(__file__).resolve().parent.parent / "data" / "weather_forecast.json"

CITY = "Hoboken"
UNITS = "imperial"
API_KEY = get_openweathermap_api_key()
FORECAST_FILE = weather_json_file

tomorrow = datetime.now().date() + timedelta(days=1)
today = tomorrow.strftime("%Y-%m-%d")


def open_forecast_file():
    """Open the JSON file read-only."""
    with open(FORECAST_FILE, 'r', encoding='utf-8') as file:
        weather_data = json.load(file)
    return weather_data

def get_weather_forecast():
    """Openweathermap API request to pull data based on city. Outputs data as JSON file."""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&units={UNITS}&appid={API_KEY}"
    try:
        response = requests.get(url, timeout=20)
        data = response.json()
    except requests.exceptions.Timeout:
        print("openweathermap API timed out")

    # Overwrite file with newest data
    with open(FORECAST_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    return data


def check_lightrain_forecast(weather_data, today, tomorrow):
    """If there is any light to moderate rain, checks for keywords from openweathermap API
    data for minor rain."""

    moderate_rain = ['moderate', 'light','clear']
    moderate_rain_time = []

    for forecast in weather_data['list']:
        forecast_date = datetime.fromtimestamp(forecast['dt']).date()
        if forecast_date.strftime("%Y-%m-%d") == today:
            for word in moderate_rain:
                if word in forecast['weather'][0]['description']:
                    moderate_rain_time.append(forecast["dt_txt"])
    msg = (
        f'Please check your local forecast for light rain in your location. '
        f'There may be light to moderate rain today/tomorrow at these times:{moderate_rain_time}'
    )
    if moderate_rain_time:
        return msg
    elif not moderate_rain_time:
        return "No rain for a few days!"

def check_thunderstorm_forecast(weather_data, today, tomorrow):
    """If there is any heavy rain, checks for keywords from openweathermap API
    data for heavy rain."""

    heavy_rain = ['heavy', 'thunderstorm', 'extreme']
    heavy_rain_time = []

    for forecast in weather_data['list']:
        forecast_date = datetime.fromtimestamp(forecast['dt']).date()
        if forecast_date.strftime("%Y-%m-%d") == today:
            for word in heavy_rain:
                if word in forecast['weather'][0]['description']:
                    heavy_rain_time.append(forecast["dt_txt"])
    msg = (
        f'Please check your local forecast for flooding in your location. '
        f'Rain will be heavier rain today/tomorrow at these times:{heavy_rain_time}'
    )

    if heavy_rain_time:
        return msg
    elif not heavy_rain_time:
        return "No heavy rain for a few days!"