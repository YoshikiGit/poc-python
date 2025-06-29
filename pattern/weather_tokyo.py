# This script will fetch and display the weather forecast for Tokyo.
import requests

def get_weather_forecast():
    # Using Open-Meteo API for weather forecast
    # API documentation: https://open-meteo.com/en/docs
    api_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 35.6895,  # Tokyo latitude
        "longitude": 139.6917, # Tokyo longitude
        "daily": "weathercode,temperature_2m_max,temperature_2m_min",
        "timezone": "Asia/Tokyo",
        "forecast_days": 7
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def display_weather_forecast(forecast_data):
    if not forecast_data or "daily" not in forecast_data:
        print("Could not retrieve weather forecast.")
        return

    daily_data = forecast_data["daily"]
    dates = daily_data.get("time", [])
    max_temps = daily_data.get("temperature_2m_max", [])
    min_temps = daily_data.get("temperature_2m_min", [])
    # weather_codes = daily_data.get("weathercode", []) # Example, can be used for more detailed descriptions

    print("Weather Forecast for Tokyo (Next 7 Days):\n")
    for i in range(len(dates)):
        date = dates[i]
        max_temp = max_temps[i] if i < len(max_temps) else "N/A"
        min_temp = min_temps[i] if i < len(min_temps) else "N/A"
        # In a real application, map weather_codes to human-readable descriptions
        print(f"Date: {date}")
        print(f"  Max Temperature: {max_temp}°C")
        print(f"  Min Temperature: {min_temp}°C")
        # print(f"  Weather: {weather_codes[i]}") # Placeholder for weather description
        print("-" * 20)

if __name__ == "__main__":
    forecast = get_weather_forecast()
    if forecast:
        display_weather_forecast(forecast)
