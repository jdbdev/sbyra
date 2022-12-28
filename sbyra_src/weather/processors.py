import environ
import requests
from django.contrib.sites.shortcuts import get_current_site

env = environ.Env()
environ.Env.read_env()


def weather_api(request):

    """
    API call to openweathermap.org and return a context dictionary

    Values returned in Metric (temp = Celcius, Wind speeds = meters/sec)
    API does not always return key values. Functions check for keys:values to prevent errors and convert wind speed and wind gusts from meters/second to knots (kt, kn). Values rounded to 2 decimal places.

    """

    # request parameters (using params from the Request library instead of f formating the url string)
    city = "Shediac"
    units = "metric"
    api_key = env("WEATHER_API")
    payload = {
        "q": city,
        "units": units,
        "appid": api_key,
    }
    r = requests.get(
        "http://api.openweathermap.org/data/2.5/weather", params=payload
    ).json()

    # conversion factor for meters/sec to knots
    conversion = float(1.9438444924)

    def wind_speed():
        """verifies that api returns a key:value and converts wind value from m/s to knots"""
        key = "speed"
        wind_speed = "unknown"

        if key in r["wind"]:
            wind_speed = float(r["wind"][key]) * conversion
            return round(wind_speed, 2)
        else:
            return wind_speed

    def wind_direction():
        """verifies that api returns a value, and provides the verbose direction from degrees"""
        key = "deg"
        wind_direction = "unknown"

        if key in r["wind"]:
            wind_direction = r["wind"][key]
        return wind_direction

    def wind_gust():
        """verifies that api returns and value and converts value from m/s to knots"""
        key = "gust"
        wind_gust = "unknown"

        if key in r["wind"]:
            wind_gust = r["wind"]["gust"]
        return wind_gust

    weather = {
        "city": city,
        "temperature": r["main"]["temp"],
        "description": r["weather"][0]["description"],
        "icon": r["weather"][0]["icon"],
        "wind_speed": wind_speed(),
        "wind_direction": wind_direction(),
        "wind_gust": wind_gust(),
    }

    return {
        "weather": weather,
    }
