import pyfao56 as fao
from pyfao56.tools import forecast
import numpy as np
import os
from osgeo import gdal, ogr, osr
import pandas as pd
from  datetime import datetime, timedelta
import requests
from shapely.wkt import loads
import rasterio
import rasterio.mask as msk
from pyproj import Transformer
from shapely.geometry import mapping

import math

def convert_wind_speed(wind_speed_10m):
    ws_2m = []
    for i in wind_speed_10m:
        if i != None:
            ws_2m.append(i * (math.log(2 / 0.0002) / math.log(10 / 0.0002)) / 3600)
        else:
            ws_2m.append(None)
    return ws_2m

def calculate_vapor_pressure_dew_point(T_dew):
    return 6.11 * 10**((7.5 * T_dew) / (T_dew + 237.3))

def get_final_date(response):

    data = response.json()
    daily_data = data.get('daily', {})
    rain_sum = daily_data.get('rain_sum', [])
    shortwave_radiation_sum = daily_data.get('shortwave_radiation_sum', [])
    et0_evapotranspiration = daily_data.get('et0_fao_evapotranspiration', [])
    temperature_max = daily_data.get('temperature_2m_max', [])
    temperature_min = daily_data.get('temperature_2m_min', [])
    rh_max = daily_data.get('relative_humidity_2m_max', [])
    tdew = data['hourly']['dewpoint_2m']
    rh_min = daily_data.get('relative_humidity_2m_min', [])
    wind_speed_max = daily_data.get('wind_speed_10m_max', [])
    Tdew = []
    Vapr = []
    i  = 0
    tdew = np.array(tdew, dtype=float)  

    while i < (len(tdew)):
        daily_mean = float(np.nanmean(tdew[i:i + 24]))  # Averaging every 24 hours
        Vapr.append(calculate_vapor_pressure_dew_point(daily_mean))
        Tdew.append(daily_mean)  # Averaging every 24 hours
        i = i + 24

    return {
        "Srad" : shortwave_radiation_sum,
        "Tmax" : temperature_max,
        "Tmin" : temperature_min,
        "Vapr" : Vapr,
        "Tdew" : Tdew,
        "RHmax": rh_max,
        "RHmin": rh_min,
        "Rain" : rain_sum,
        "ETref": et0_evapotranspiration,
        "MorP" : ["M"] * len(rain_sum),
        "Wndsp": convert_wind_speed(wind_speed_max)
        }, daily_data.get('time')


def fao_Open_meteo(forcast_Data,start_date, end_date, lat, long):
    # Set the URL for the Open-Meteo API (historical data)
    url = "https://archive-api.open-meteo.com/v1/archive"

    # Define parameters for the API request
    params = {
        "latitude": lat,  # Replace with the latitude of your location
        "longitude": long,  # Replace with the longitude of your location
        "start_date": start_date,  # Start date for historical data
        "end_date": end_date,  # End date for historical data
        "daily" : "rain_sum,shortwave_radiation_sum,et0_fao_evapotranspiration,temperature_2m_max,temperature_2m_min,relative_humidity_2m_max,relative_humidity_2m_min,wind_speed_10m_max",
        "hourly": "dewpoint_2m",
        "timezone": "Africa/Casablanca"  # Set your timezone
    }


    # Send the request to the Open-Meteo API
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data, dates = get_final_date(response)

        for key in data:
            if data[key][-1] == None \
                or data[key][-1] == np.nan:
                data[key][-1] = forcast_Data[key][0] 
            data[key] +=  forcast_Data.get(key, [])
    
        return data

    else:
        print(f"Error: {response.status_code}")

def forcast_fao_Open_meteo(lat, long):
    # Set the URL for the Open-Meteo API (historical data)
    url = "https://api.open-meteo.com/v1/forecast"

    # Define parameters for the API request
    params = {
        "latitude": lat,  # Replace with the latitude of your location
        'forecast_days' : '5',
        "longitude": long,  # Replace with the longitude of your location
        "daily" : "rain_sum,shortwave_radiation_sum,et0_fao_evapotranspiration,temperature_2m_max,temperature_2m_min,relative_humidity_2m_max,relative_humidity_2m_min,wind_speed_10m_max,wind_direction_10m_dominant",
        "hourly": "dewpoint_2m",
        "timezone": "Africa/Casablanca"  # Set your timezone
    }


    # Send the request to the Open-Meteo API
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        return  get_final_date(response)

    else:
        print(f"Error: {response.status_code}")


