import requests
from  datetime import datetime, timedelta
import pandas as pd
from aquacrop import AquaCropModel, Soil, Crop, InitialWaterContent, IrrigationManagement
import math
from scipy.interpolate import interp1d
import numpy as np


def fill_missing_values(data, method='mean'):
    """
    Fill missing values in a list using averages or interpolation.
    """
    if not data:
        return data

    # Convert None to NaN for easier handling
    data = np.array(data, dtype=float)
    mask = np.isnan(data)

    if method == 'mean':
        # Fill missing values with the mean of available data
        mean_value = np.nanmean(data)
        data[mask] = mean_value
    elif method == 'interpolate':
        # Interpolate missing values
        x = np.arange(len(data))
        interp_fn = interp1d(x[~mask], data[~mask], kind='linear', fill_value="extrapolate")
        data[mask] = interp_fn(x[mask])

    return data.tolist()

def convert_wind_speed(wind_speed_10m):
    """
    Convert wind speed from 10m height to 2m height using a logarithmic wind profile.
    """
    if wind_speed_10m is None:
        return None
    return wind_speed_10m * (math.log(2 / 0.0002) / (math.log(10 / 0.0002)))

def historic_weather(lat, lon, start_date, end_date):

    historic_forecast_url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    historic_url = "https://archive-api.open-meteo.com/v1/archive"

    params = {

        "latitude": lat,  
        "longitude": lon,  
        "start_date": start_date,  
        "end_date": end_date,
        "daily": ("rain_sum,shortwave_radiation_sum,et0_fao_evapotranspiration,"
                  "temperature_2m_max,relative_humidity_2m_max,"
                  "wind_speed_10m_max,wind_direction_10m_dominant"),
        "hourly": "wind_speed_10m,wind_direction_10m",
        "timezone": "Africa/Casablanca", 
        "windspeed_unit": "ms",
    }

    # Get archive (historical) data
    response = requests.get(historic_url, params=params)
    response.raise_for_status()
    data = response.json()

    # Retrieve daily and hourly parts
    daily = data.get('daily', {})
    hourly = data.get('hourly', {})

    # Define the keys to check for daily and hourly data
    daily_keys = [
        "rain_sum",
        "shortwave_radiation_sum",
        "et0_fao_evapotranspiration",
        "temperature_2m_max",
        "relative_humidity_2m_max",
        "wind_speed_10m_max",
        "wind_direction_10m_dominant"
    ]
    hourly_keys = [
        "wind_speed_10m",
        "wind_direction_10m"
    ]

    # Build dictionaries for daily and hourly data
    daily_data = {key: daily.get(key, []) for key in daily_keys}
    hourly_data = {key: hourly.get(key, []) for key in hourly_keys}

    # Check for missing values in daily data
    missing_daily_indices = set()
    for key in daily_keys:
        for idx, value in enumerate(daily_data[key]):
            if value is None:
                missing_daily_indices.add(idx)

    # Check for missing values in hourly data
    missing_hourly_indices = set()
    for key in hourly_keys:
        for idx, value in enumerate(hourly_data[key]):
            if value is None:
                missing_hourly_indices.add(idx)

    # If there are missing values in either daily or hourly data, patch from forecast
    if missing_daily_indices or missing_hourly_indices:
        response = requests.get(historic_forecast_url, params=params)
        response.raise_for_status()
        forecast_data = response.json()

        # Patch daily missing values
        forecast_daily = forecast_data.get('daily', {})
        for key in daily_keys:
            forecast_values = forecast_daily.get(key, [])
            for idx in missing_daily_indices:
                if idx < len(forecast_values) and forecast_values[idx] is not None:
                    daily_data[key][idx] = forecast_values[idx]

        # Patch hourly missing values
        forecast_hourly = forecast_data.get('hourly', {})
        for key in hourly_keys:
            forecast_values = forecast_hourly.get(key, [])
            for idx in missing_hourly_indices:
                if idx < len(forecast_values) and forecast_values[idx] is not None:
                    hourly_data[key][idx] = forecast_values[idx]

    return {
            "Dates"     : daily['time'],
            "Rain"      : daily_data["rain_sum"],
            "irg"       : daily_data["shortwave_radiation_sum"],
            "Et0"       : daily_data["et0_fao_evapotranspiration"],
            "T2m_max"   : daily_data["temperature_2m_max"],
            "Rh_max"    : daily_data["relative_humidity_2m_max"],
            "Ws"        : daily_data["wind_speed_10m_max"],
            "Wd"        : daily_data["wind_direction_10m_dominant"],
            'ws_h'      : hourly_data["wind_speed_10m"],
            'wd_h'      : hourly_data["wind_direction_10m"]
    }

def forcast(lat, lon):

    url = "https://api.open-meteo.com/v1/forecast"

    # Define parameters for the API request
    params = {
        "latitude": lat,
        'forecast_days' : '7',
        "longitude": lon,  
        "daily" : "rain_sum,shortwave_radiation_sum,et0_fao_evapotranspiration,temperature_2m_max,relative_humidity_2m_max,wind_speed_10m_max,wind_direction_10m_dominant,precipitation_probability_mean",
        "timezone": "Africa/Casablanca", 
        "windspeed_unit": "ms",        # kmh, ms, mph, kn
    }


    # Send the request to the Open-Meteo API
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an error for bad responses

    # Check if the request was successful
    data = response.json()


    daily = data['daily']

    return {
            "Dates"             : daily['time'],
            "Rain"              : daily["rain_sum"],
            "irg"               : daily["shortwave_radiation_sum"],
            "Et0"               : daily["et0_fao_evapotranspiration"],
            "T2m_max"           : daily["temperature_2m_max"],
            "Rh_max"            : daily["relative_humidity_2m_max"],
            "Ws"                : [convert_wind_speed(ws) for ws in daily["wind_speed_10m_max"]],
            "Wd"                : daily["wind_direction_10m_dominant"],
            "Rain_pro"          : daily["precipitation_probability_mean"],
    }

def gdd_weather(lat, lon, start_date, end_date):

    Tbase = 0
    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": lat,  
        "longitude": lon,  
        "start_date": start_date,  
        "end_date": end_date,  # End date for historical data
        # "hourly": "temperature_2m,precipitation,wind_speed_10m,relative_humidity_2m,shortwave_radiation",  # Request hourly data for temperature, precipitation, wind speed, RH, and shortwave radiation
        "daily" : "temperature_2m_max,temperature_2m_min",
        "timezone": "Africa/Casablanca", 
        "windspeed_unit": "ms",        # kmh, ms, mph, kn
    }

    response = requests.get(url, params=params)

    response.raise_for_status()
    
    data = response.json()

    Tmax = data.get('daily')["temperature_2m_max"]
    Tmin = data.get('daily')["temperature_2m_min"]

    len_, i, gdd = len(Tmax), 0, []

    while(i < len_):
        daily_gdd = max(((Tmax[i] + Tmin[i]) / 2) - Tbase, 0)
        gdd.append(daily_gdd)
        i += 1

    gdd_cum = []
    cumulative = 0
    start = datetime.strptime(start_date, "%Y-%m-%d")
    current_date = start
    zero, Emergence, Developpement_foliaire, tallage, Allongement_de_la_tige, Floraison, Remplissage_des_graines, Stade_pate, Maturite_complete = [], [], [], [], [], [], [], [], []
    stages = [
        (125, zero),
        (160, Emergence),
        (208, Developpement_foliaire),
        (421, tallage),
        (659, Allongement_de_la_tige),
        (901, Floraison),
        (1174, Remplissage_des_graines),
        (1556, Stade_pate),
        (float('inf'), Maturite_complete),
    ]

    for value in gdd:
        cumulative += value
        for threshold, stage_list in stages:
            if cumulative <= threshold:
                stage_list.append(current_date.strftime("%Y-%m-%d"))
                break
        gdd_cum.append(cumulative)
        current_date += timedelta(days=1)
    
    return {
            'gdd'	: gdd_cum,
            'dates'	: [zero, Emergence, Developpement_foliaire,
                        tallage, Allongement_de_la_tige, Floraison,
                            Remplissage_des_graines, Stade_pate, Maturite_complete],
        }

def calcul_aquacrop(lat, lon, start_date, end_date):

    url = "https://archive-api.open-meteo.com/v1/archive"

    # Define parameters for the API request
    params = {
        "latitude": lat,  
        "longitude": lon,  
        "start_date": start_date,  
        "end_date": end_date,  # End date for historical data
        "daily" : "precipitation_sum,et0_fao_evapotranspiration,temperature_2m_max,temperature_2m_min",
        "timezone": "Africa/Casablanca", 
        "windspeed_unit": "ms",        # kmh, ms, mph, kn
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an error for bad responses

    # Check if the request was successful
    data = response.json()

    daily_data = data['daily']

    dates = pd.date_range(start=start_date, end=end_date, freq='D').tolist()

    # print(dates)
    data = pd.DataFrame({'MinTemp' : daily_data['temperature_2m_min'],
            'MaxTemp' : daily_data['temperature_2m_max'],
            'Precipitation' : daily_data['precipitation_sum'],
            'ReferenceET' : daily_data['et0_fao_evapotranspiration'],
            'Date' : dates,
        })
    
    model_os = AquaCropModel(
            sim_start_time=datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y/%m/%d'),
            sim_end_time=datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y/%m/%d'),
            weather_df=data,
            soil=Soil(soil_type='SandyLoam'),
            crop=Crop('Maize', planting_date=f"{start_date.split('-')[1]}/{start_date.split('-')[2]}"),
            irrigation_management=IrrigationManagement(irrigation_method=4),
            initial_water_content=InitialWaterContent(value=['FC']),
        )

    model_os.run_model(till_termination=True)
    # Water_flux = model_os.get_water_flux()[['IrrDay', 'Tr', 'DeepPerc', 'Es']]
    crop_growth = model_os.get_crop_growth()[['gdd_cum', 'canopy_cover', 'biomass', 'DryYield', 'YieldPot']]

    return {
        'gdd_cum'       : crop_growth.gdd_cum.values,
        'canopy_cover'  : crop_growth.canopy_cover.values,
        'biomass'       : crop_growth.biomass.values,
        'DryYield'      : crop_growth.DryYield.values,
        'YieldPot'      : crop_growth.YieldPot.values,
    }
    # return {
    #     'dates' : date_strings,
    #     'IrrDay' : Water_flux.IrrDay.values,
    #     'Tr' : Water_flux.Tr.values,
    #     'DeepPerc' : Water_flux.DeepPerc.values,
    #     'Es' : Water_flux.Es.values,
    #     'Th1' : water_storage.th1.values,
    #     'Th2' : water_storage.th2.values,
    #     'th3' : water_storage.th3.values,
    #     'gdd_cum' : crop_growth.gdd_cum.values,
    #     'canopy_cover' : crop_growth.canopy_cover.values,
    #     'biomass' : crop_growth.biomass.values,
    #     'z_root' : crop_growth.z_root.values,
    #     'DryYield' : crop_growth.DryYield.values,
    #     'FreshYield' : crop_growth.FreshYield.values,
    #     'harvest_index' : crop_growth.harvest_index.values,
    #     'ET' : Water_flux.Tr.values + Water_flux.Es.values,
    # }

if __name__ == '__main__':
    # calcul_aquacrop(31.665795547539773, -7.678333386926454, '2024-01-01', '2024-05-05')
    print(forcast(31.665795547539773, -7.678333386926454))
    # print(historic_weather(31.665795547539773, -7.678333386926454, '2024-11-01', '2024-11-28'))