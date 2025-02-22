import requests
from  datetime import datetime, timedelta
import pandas as pd
from aquacrop import AquaCropModel, Soil, Crop, InitialWaterContent, IrrigationManagement
import math
from scipy.interpolate import interp1d
import numpy as np

def convert_wind_speed(wind_speed_10m):
    """
    Convert wind speed from 10m height to 2m height using a logarithmic wind profile.
    """
    if wind_speed_10m is None:
        return None
    return round(wind_speed_10m * (math.log(2 / 0.0002) / (math.log(10 / 0.0002))), 2)

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
        "timezone": "Africa/Casablanca", 
        "windspeed_unit": "ms",
    }

    # Get archive (historical) data
    response = requests.get(historic_url, params=params)
    response.raise_for_status()
    data = response.json()

    # Retrieve daily and hourly parts
    daily_data = data.get('daily', {})
    # print(daily_data)
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


    missing_indices_per_variable = {
            key: [idx for idx, value in enumerate(daily_data[key]) if value is None]
            for key in daily_keys
    }
    if missing_indices_per_variable:
        response = requests.get(historic_forecast_url, params=params)
        response.raise_for_status()
        forecast_data = response.json()

        # Patch daily missing values
        forecast_daily = forecast_data.get('daily', {})
        for key, missing_indices in missing_indices_per_variable.items():
            if missing_indices_per_variable[key]:
                for idx in missing_indices:
                    daily_data[key][idx] = forecast_daily[key][idx]

    return {
            "Dates"     : forecast_daily['time'],
            "Rain"      : daily_data["rain_sum"],
            "irg"       : daily_data["shortwave_radiation_sum"],
            "Et0"       : daily_data["et0_fao_evapotranspiration"],
            "T2m_max"   : daily_data["temperature_2m_max"],
            "Rh_max"    : daily_data["relative_humidity_2m_max"],
            "Ws"        : [convert_wind_speed(ws) for ws in daily_data["wind_speed_10m_max"]],
            "Wd"        : daily_data["wind_direction_10m_dominant"],
    }

def forcast(lat, lon):

    url = "https://api.open-meteo.com/v1/forecast"

    # Define parameters for the API request
    params = {
        "latitude": lat,
        'forecast_days' : '7',
        "longitude": lon,  
        "daily" : "rain_sum,shortwave_radiation_sum,et0_fao_evapotranspiration,temperature_2m_max,temperature_2m_min,relative_humidity_2m_max,wind_speed_10m_max,wind_direction_10m_dominant,precipitation_probability_mean",
        "timezone": "Africa/Casablanca",
        "hourly": "wind_speed_10m,wind_direction_10m,cloud_cover",
        "windspeed_unit": "ms",        # kmh, ms, mph, kn
    }


    # Send the request to the Open-Meteo API
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an error for bad responses

    # Check if the request was successful
    data = response.json()


    daily   = data['daily']
    hourly  = data['hourly']
    
    daily_avg = []
    for i in range(0, len(hourly['cloud_cover']), 24):
        day_values = hourly['cloud_cover'][i:i+24]
        daily_avg.append(sum(day_values) / 24)
    
    return {
            "Dates"             : daily['time'],
            "Rain"              : daily["rain_sum"],
            "irg"               : daily["shortwave_radiation_sum"],
            "Et0"               : daily["et0_fao_evapotranspiration"],
            "T2m_max"           : daily["temperature_2m_max"],
            "T2m_min"           : daily["temperature_2m_min"],
            "Rh_max"            : daily["relative_humidity_2m_max"],
            "Ws"                : [convert_wind_speed(ws) for ws in daily["wind_speed_10m_max"]],
            "Wd"                : daily["wind_direction_10m_dominant"],
            "Rain_pro"          : daily["precipitation_probability_mean"],
            "Ws_h"              : hourly['wind_speed_10m'][:24],
            'Wd_h'              : hourly['wind_direction_10m'][:24],
            'cloud'             : daily_avg,
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