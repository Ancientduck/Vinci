import requests

def fetch_weather_data():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 24.3636,
        "longitude": 88.6241,
        "current": ["temperature_2m", "relative_humidity_2m", "precipitation_probability", "wind_speed_10m", "wind_direction_10m"],
        "timezone": "auto"
    }

    response = requests.get(url, params=params)
    data = response.json()
    
    current = data["current"]
    units = data["current_units"]

    summary = (
        f"--- Weather Summary for Rajshahi ---\n"
        f"Temperature: {current['temperature_2m']}{units['temperature_2m']}\n"
        f"Humidity: {current['relative_humidity_2m']}{units['relative_humidity_2m']}\n"
        f"Precipitation Probability: {current['precipitation_probability']}{units['precipitation_probability']}\n"
        f"Wind Speed: {current['wind_speed_10m']}{units['wind_speed_10m']}\n"
        f"Wind Direction: {current['wind_direction_10m']}{units['wind_direction_10m']}"
    )

    print(summary)

def main():
    fetch_weather_data()

if __name__ == "__main__":
    main()