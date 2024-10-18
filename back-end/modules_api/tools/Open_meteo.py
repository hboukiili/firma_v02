import requests
from datetime import datetime, timedelta
import math
# from meteo_ET0 import et0_pm, et0_pm_simple
import numpy as np
import pandas as pd

def convert_wind_speed(wind_speed_10m):
    
    ws_2m = []
    for i in wind_speed_10m:
        ws_2m.append(i * (math.log(2 / 0.0002) / math.log(10 / 0.0002)))
    return ws_2m

def Open_meteo(start_date, end_date, lat, long):
    # Set the URL for the Open-Meteo API (historical data)
    url = "https://archive-api.open-meteo.com/v1/archive"

    # Define parameters for the API request
    params = {
        "latitude": lat,  # Replace with the latitude of your location
        "longitude": long,  # Replace with the longitude of your location
        "start_date": start_date,  # Start date for historical data
        "end_date": end_date,  # End date for historical data
        "hourly": "temperature_2m,precipitation,wind_speed_10m,relative_humidity_2m,shortwave_radiation",  # Request hourly data for temperature, precipitation, wind speed, RH, and shortwave radiation
        "timezone": "Africa/Casablanca"  # Set your timezone
    }


    # Send the request to the Open-Meteo API
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Access the hourly data for each variable
        temperature_2m = data['hourly']['temperature_2m']
        precipitation = data['hourly']['precipitation']
        wind_speed = data['hourly']['wind_speed_10m']
        relative_humidity_2m = data['hourly']['relative_humidity_2m']
        shortwave_radiation = data['hourly']['shortwave_radiation']
        hours = data['hourly']['time']  # The list of times for each hourly value

        i = 0
        days_data = {}
        wind_speed = convert_wind_speed(wind_speed)
        # dates = []

        while i < (len(hours)):
            day = datetime.strptime(hours[i], '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d')
            
            if day not in days_data:
                days_data[day] = {
                    "T2m": [],
                    "Pre": [],
                    "Ws": [],
                    "Rh": [],
                    "Irg": [],
                }
    
            days_data[day]["T2m"].append(temperature_2m[i : i + 24])
            days_data[day]["Pre"].append(precipitation[i : i + 24])
            days_data[day]["Ws"].append(wind_speed[i : i + 24])
            days_data[day]["Rh"].append(relative_humidity_2m[i : i + 24])
            days_data[day]["Irg"].append(shortwave_radiation[i : i + 24])
            # dates.append(day)
            i = i + 24

    else:
        print(f"Error: {response.status_code}")

    return days_data