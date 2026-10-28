
import os
import requests

from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv()

GEO_URL = "https://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


@tool
def get_weather(city: str) -> dict:
    """Get current weather information for a city.
    Example: Lahore,PK or Karachi,PK.
    """

    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        return {"error": "OPENWEATHER_API_KEY is missing from .env."}

    if not city or not city.strip():
        return {"error": "Please provide a valid city name."}

    city = city.strip()

    try:
        # 1. Find the city's coordinates
        geo_response = requests.get(
            GEO_URL,
            params={
                "q": city,
                "limit": 5,
                "appid": api_key,
            },
            timeout=15,
        )

        geo_response.raise_for_status()
        locations = geo_response.json()

        if not locations:
            return {
                "error": f"City '{city}' was not found. Try adding a country code."
            }

        location = locations[0]
        lat = location.get("lat")
        lon = location.get("lon")

        if lat is None or lon is None:
            return {"error": "Could not resolve city coordinates."}

        # 2. Fetch weather using coordinates
        response = requests.get(
            WEATHER_URL,
            params={
                "lat": lat,
                "lon": lon,
                "appid": api_key,
                "units": "metric",
            },
            timeout=15,
        )

        response.raise_for_status()
        data = response.json()

        main = data.get("main", {})
        weather = data.get("weather", [])
        wind = data.get("wind", {})
        system = data.get("sys", {})

        if "temp" not in main or not weather:
            return {"error": "The weather API returned incomplete data."}

        # 3. Convert observation time to local time
        observed_at = None
        timestamp = data.get("dt")
        offset = data.get("timezone", 0)

        if timestamp is not None:
            local_timezone = timezone(timedelta(seconds=offset))
            observed_at = datetime.fromtimestamp(
                timestamp, tz=timezone.utc
            ).astimezone(local_timezone).isoformat()

        return {
            "source": "OpenWeatherMap",
            "city": data.get("name", location.get("name")),
            "state": location.get("state"),
            "country": system.get("country", location.get("country")),
            "coordinates": {
                "latitude": lat,
                "longitude": lon,
            },
            "temperature_c": main.get("temp"),
            "feels_like_c": main.get("feels_like"),
            "min_temperature_c": main.get("temp_min"),
            "max_temperature_c": main.get("temp_max"),
            "humidity_percent": main.get("humidity"),
            "condition": weather[0].get("description"),
            "condition_group": weather[0].get("main"),
            "wind_speed_m_s": wind.get("speed"),
            "wind_direction_degrees": wind.get("deg"),
            "pressure_hpa": main.get("pressure"),
            "cloudiness_percent": data.get("clouds", {}).get("all"),
            "visibility_m": data.get("visibility"),
            "observed_at_local": observed_at,
        }

    except requests.Timeout:
        return {"error": "Weather API timed out. Please try again."}

    except requests.HTTPError as e:
        status = e.response.status_code if e.response is not None else None

        if status == 401:
            message = "Invalid or inactive OpenWeather API key."
        elif status == 404:
            message = "Weather or location data was not found."
        elif status == 429:
            message = "OpenWeather API rate limit exceeded."
        else:
            message = f"Weather API HTTP error: {status}."

        return {"error": message}

    except (requests.RequestException, ValueError, KeyError) as e:
        return {"error": f"Could not retrieve weather data: {e}"}
