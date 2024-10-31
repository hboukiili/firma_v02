import requests
from datetime import datetime, timedelta
import math
from meteo_ET0 import et0_pm, et0_pm_simple
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
        print(data)
        days_data = {}
        wind_speed = convert_wind_speed(wind_speed)
        dates = []

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
            dates.append(day)
            i = i + 24
        # for i in days_data:
            # print(i, days_data[i])
    else:
        print(f"Error: {response.status_code}")

    return days_data, dates


start_date  = "2022-02-01"
end_date    = "2022-05-01"
lat         = 32.2355
long        = -7.9533
alt         = 398

Weather_data, Dates = Open_meteo(start_date, end_date, lat, long)

start_date_ = datetime.strptime(start_date, '%Y-%m-%d')
end_date_ = datetime.strptime(end_date, '%Y-%m-%d')
current_date = start_date_
et0_, T_min, T_max, pre, dates = [], [], [], [], []

while current_date <= end_date_:

        current_date_str = current_date.strftime("%Y-%m-%d")
        t_min = np.nanmin(Weather_data[current_date_str]["T2m"])
        t_max = np.nanmax(Weather_data[current_date_str]["T2m"])
        et0_simple = et0_pm_simple(
            current_date.timetuple().tm_yday, 
            alt, 
            2, 
            lat, 
            np.nanmean(Weather_data[current_date_str]["T2m"]), 
            t_min,  
            t_max,
            np.nanmean(Weather_data[current_date_str]["Ws"]), 
            np.nanmean(Weather_data[current_date_str]["Rh"]), 
            np.nanmin(Weather_data[current_date_str]["Rh"]),   
            np.nanmax(Weather_data[current_date_str]["Rh"]),  
            np.nanmean(Weather_data[current_date_str]["Irg"])
        )
        
        et0_.append(et0_simple)
        T_max.append(t_max)
        T_min.append(t_min)
        pre.append(np.nanmean(Weather_data[current_date_str]["Pre"]))
        dates.append(current_date)
        current_date += timedelta(days=1)

data = pd.DataFrame({'MinTemp' : T_min,
        'MaxTemp' : T_max,
        'Precipitation' : pre,
        'ReferenceET' : et0_,
        'Date' : dates,
    })

# print(data)

from aquacrop import AquaCropModel, Soil, Crop, InitialWaterContent

model_os = AquaCropModel(
        sim_start_time=start_date_.strftime('%Y/%m/%d'),
        sim_end_time=end_date_.strftime('%Y/%m/%d'),
        weather_df=data,
        soil=Soil(soil_type='SandyLoam'),
        crop=Crop('Maize', planting_date=start_date_.strftime('%m/%d')),
        # irrigation_management=IrrigationManagement(irrigation_method=4),
        initial_water_content=InitialWaterContent(value=['FC']),
    )


model_os.run_model(till_termination=True)
Water_flux = model_os.get_water_flux()[['IrrDay', 'Tr', 'DeepPerc', 'Es']]
water_storage = model_os.get_water_storage()[['th1', 'th2', 'th3']]
crop_growth = model_os.get_crop_growth()[['gdd_cum', 'canopy_cover', 'biomass', 'z_root', 'DryYield', 'FreshYield', 'harvest_index']]

print(water_storage)