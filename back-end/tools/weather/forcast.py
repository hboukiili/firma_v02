# import openmeteo_requests
# import requests_cache
# import pandas as pd
# from retry_requests import retry
# from datetime import datetime, timedelta
# import numpy as np
# from openmeteo_sdk.Variable import Variable

# pd.set_option('display.max_rows', None)  # This will display all rows
# pd.set_option('display.max_columns', None)  # This will display all columns

# # Setup the Open-Meteo API client with cache and retry on error
# cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
# retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
# openmeteo = openmeteo_requests.Client(session = retry_session)

# # Make sure all required weather variables are listed here
# # The order of variables in hourly or daily is important to assign them correctly below
# url = "https://api.open-meteo.com/v1/forecast"

# params = {
# 	"latitude": 32.243,
# 	"longitude": -7.9596,
#     # "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",  # Request multiple daily variables
# 	"hourly": ["temperature_2m", "precipitation", "wind_speed_10m", "et0_fao_evapotranspiration"],
# 	"timezone" : "Africa/Casablanca"
# }

# responses = openmeteo.weather_api(url, params=params)

# # Process first location. Add a for-loop for multiple locations or weather models
# response = responses[0]
# hourly = response.Hourly()
# hourly_time = range(hourly.Time(), hourly.TimeEnd(), hourly.Interval())
# hourly_variables = list(map(lambda i: hourly.Variables(i), range(0, hourly.VariablesLength())))

# # Print all variables to check what's available
# for variable in hourly_variables:
#     print("Variable:", variable.Variable(), "Altitude:", variable.Altitude())


# hourly_temperature_2m = next(filter(lambda x: x.Variable() == Variable.temperature and x.Altitude() == 2, hourly_variables)).ValuesAsNumpy()
# hourly_precipitation = next(filter(lambda x: x.Variable() == Variable.precipitation, hourly_variables)).ValuesAsNumpy()
# hourly_wind_speed_10m = next(filter(lambda x: x.Variable() == Variable.wind_speed and x.Altitude() == 10, hourly_variables)).ValuesAsNumpy()
# hourly_et0_fao_evapotranspiration = next(filter(lambda x: x.Variable() == Variable.et0_fao_evapotranspiration, hourly_variables)).ValuesAsNumpy()

# hourly_data = {"date": pd.date_range(
# 	start = pd.to_datetime(hourly.Time(), unit = "s"),
# 	end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
# 	freq = pd.Timedelta(seconds = hourly.Interval()),
# 	inclusive = "left"
# )}

# hourly_data["temperature_2m"] = hourly_temperature_2m
# hourly_data["precipitation"] = hourly_precipitation
# hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
# hourly_data["et0_fao_evapotranspiration"] = hourly_et0_fao_evapotranspiration

# hourly_dataframe = pd.DataFrame(data = hourly_data)
# print(hourly_dataframe)

# # print(Daily_temperature_2m_max)
# # Daily_temperature_2m_min = Daily.Variables(1).ValuesAsNumpy()
# # Daily_temperature_2m_precipitation_sum = Daily.Variables(2).ValuesAsNumpy()

# # Daily_data = {"date": pd.date_range(
# # 	start = pd.to_datetime(Daily.Time(), unit = "s", utc = True),
# # 	end = pd.to_datetime(Daily.TimeEnd(), unit = "s", utc = True),
# # 	freq = pd.Timedelta(seconds = Daily.Interval()),
# # 	inclusive = "left"
# # )}

# # Daily_data["temperature_2m_max"] = Daily_temperature_2m_max
# # Daily_data["temperature_2m_min"] = Daily_temperature_2m_min
# # Daily_data["precipitation_sum"] = Daily_temperature_2m_precipitation_sum

# # Daily_dataframe = pd.DataFrame(data = Daily_data)
# # print(Daily_dataframe)

import requests
from datetime import datetime

# API endpoint
url = "https://api.open-meteo.com/v1/forecast"

# Define parameters
params = {
    "latitude": 32.2355,  # Latitude for Los Angeles
    "longitude": -7.9533,  # Longitude for Los Angeles
    # "daily": "et0_fao_evapotranspiration,rain_sum",
    "hourly": "temperature_2m,wind_speed_10m,et0_fao_evapotranspiration,rain,relative_humidity_2m,dew_point_2m,visibility",  # Variables you need
    "timezone": "America/Los_Angeles",  # Timezone
}

try:
    # Send the request
	response = requests.get(url, params=params)
	response.raise_for_status()  # Raise an error for bad responses
    
    # Parse the JSON response
	forecast_data = response.json()

	hourly_data = forecast_data['hourly']
    
	timestamps = [int(datetime.strptime(date, "%Y-%m-%dT%H:%M").timestamp()) for date in hourly_data['time']]
	temperature_2m = hourly_data['temperature_2m']
	wind_speed_10m = hourly_data['wind_speed_10m']
	et0_fao_evapotranspiration = hourly_data['wind_speed_10m']
	rain = 	hourly_data['rain']
	relative_humidity_2m = hourly_data['relative_humidity_2m']
	dew_point_2m = hourly_data['dew_point_2m']
	visibility = hourly_data['visibility']

	print(visibility)
    # Example: Print hourly temperature forecast
    # temperature = hourly.get("temperature_2m", [])
    # time = hourly.get("time", [])

    # print("Hourly Forecast (Temperature in °C):")
    # for t, temp in zip(time, temperature):
    #     print(f"{t}: {temp}°C")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
