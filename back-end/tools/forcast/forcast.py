import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime, timedelta


# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 32.243,
	"longitude": -7.9596,
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",  # Request multiple daily variables
    "timezone" : "Africa/Casablanca"
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

Daily = response.Daily()
start_datetime = datetime.utcfromtimestamp(Daily.Time())
# print(start_datetime)
Daily_temperature_2m_max = Daily.Variables(0).ValuesAsNumpy()
Daily_temperature_2m_min = Daily.Variables(1).ValuesAsNumpy()
Daily_temperature_2m_precipitation_sum = Daily.Variables(2).ValuesAsNumpy()

Daily_data = {"date": pd.date_range(
	start = pd.to_datetime(Daily.Time(), unit = "s", utc = True),
	end = pd.to_datetime(Daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = Daily.Interval()),
	inclusive = "left"
)}

Daily_data["temperature_2m_max"] = Daily_temperature_2m_max
Daily_data["temperature_2m_min"] = Daily_temperature_2m_min
Daily_data["precipitation_sum"] = Daily_temperature_2m_precipitation_sum

Daily_dataframe = pd.DataFrame(data = Daily_data)
print(Daily_dataframe)