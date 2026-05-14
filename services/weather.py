import requests

def degrees_to_cardinal(degrees):
    directions = [
        "N", "NE", "E", "SE",
        "S", "SW", "W", "NW"
    ]

    index = round(degrees / 45) % 8

    return directions[index]

def fetch_weather(lat, lon):
    url = (
        "http://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        "&current=temperature_2m,"
        "wind_speed_10m,"
        "wind_direction_10m"
        "&daily=temperature_2m_max,"
        "temperature_2m_min"
        "&temperature_unit=fahrenheit"
        "&wind_speed_unit=mph"
        "&timezone=auto"
    )

    response = requests.get(url, timeout=10)

    data = response.json()

    return {
        "current_temp": data["current"]["temperature_2m"],
        "wind_speed": data["current"]["wind_speed_10m"],
        "wind_direction": data["current"]["wind_direction_10m"],
        "high": data["daily"]["temperature_2m_max"][0],
        "low": data["daily"]["temperature_2m_min"][0],
    }