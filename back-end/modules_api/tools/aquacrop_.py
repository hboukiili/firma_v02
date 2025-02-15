from aquacrop import AquaCropModel, Soil, Crop, InitialWaterContent, IrrigationManagement
from aquacrop.utils import prepare_weather, get_filepath
import pandas as pd
from .meteo_ET0 import et0_pm, et0_pm_simple
import numpy as np
import os
import requests
# from ogimet import Ogimet_class/
from  datetime import datetime, timedelta
from math import *
import math
from .ogimet import *

def calculate_dew_point(temperature, relative_humidity):
    """
    Calculate dew point temperature (Tdew) using the Magnus formula.
    
    Parameters:
        temperature (float): Air temperature in degrees Celsius.
        relative_humidity (float): Relative humidity as a percentage (0-100).
        
    Returns:
        float: Dew point temperature (Tdew) in degrees Celsius.
    """
    # Constants for the Magnus formula
    a = 17.27
    b = 237.7
    
    # Calculate the saturation vapor pressure (es) and actual vapor pressure (ea)
    es = 6.112 * 10 ** ((a * temperature) / (b + temperature))
    ea = (relative_humidity / 100) * es
    
    # Calculate the dew point temperature (Tdew) using the Magnus formula
    Tdew = (b * ((a * temperature) / (b + temperature) + np.log(ea / 6.112))) / (a - ((a * temperature) / (b + temperature) + np.log(ea / 6.112)))
    
    return Tdew

def calculate_relative_humidity(T, Tdew):
    # Calculate saturation vapor pressure at T

    e_T = 6.112 * math.exp((17.67 * T) / (T + 243.5))
    # Calculate saturation vapor pressure at Tdew
    e_Tdew = 6.112 * math.exp((17.67 * Tdew) / (Tdew + 243.5))
    # Calculate relative humidity
    RH = (e_Tdew / e_T) * 100
    return RH

def get_elevation_open(lat, lon):
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            elevation = data['results'][0]['elevation']
            return elevation
        else:
            print("No elevation data found.")
    else:
        print("Failed to get valid response, status code:", response.status_code)

def Extraterrestrial_radiation(lat,jday):
	lat_rad=lat*pi/180.
	dr=1 + 0.033 * cos(2*pi/365*jday)
	soldecl=0.409*sin((2*pi/365*jday) - 1.39)
	sunset_angle=acos(-tan(lat_rad)*tan(soldecl))
	   
	ra= (24*60/pi)* 0.082 * dr * (sunset_angle * sin(lat_rad) * sin(soldecl) + cos(lat_rad) * cos(soldecl) * sin(sunset_angle))

	return(ra)

def Solar_radiation_cloudiness(lat,jday,cF):

	const_as=0.25
	const_bs=0.5
	ra=Extraterrestrial_radiation(lat,jday)
	rs=(const_as+const_bs*cF/100.)*ra
	return(rs)

def aquacrop_run(start_date_, end_date_, Weather_data, lat, long):

    T_min = []
    T_max = []
    et0_ = []
    pre = []
    dates = []
    h = 2
    interior = 1
    albedo = 0.23
    rn = rs = n = ea =-9999    

    # if start_date_ is None:

    #     start_date_ = datetime.strptime('2019-01-01', '%Y-%m-%d')
    #     end_date_ = datetime.strptime('2019-05-01', '%Y-%m-%d')

    #     fichier = "/app/tools/aquacrop_test/chichaoua_Zoubair_2019-2023_N0_Unification.xlsx"

    #     df = pd.read_excel(fichier)

    #     df['Date'] = pd.to_datetime(df['Date'])

    #     # Group by date and apply min and max aggregation functions
    #     daily_min_max = df.groupby(df['Date'].dt.date).agg({
    #         'Chichawa_M_IDv_(°)': ['min', 'max'],
    #         'Chichawa_M_IHr_(%)': ['min', 'max', 'mean'],
    #         'Chichawa_M_IRg_(W/m2)': ['mean'],
    #         'Chichawa_M_ITair_(°C)': ['min', 'max', 'mean'],
    #         'Chichawa_M_IVv_(m/s)': ['min', 'max', 'mean'],
    #         'Chichawa_P_IP30m_(mm)': ['min', 'max']
    #     })

    #     for i in range(0, 121):

    #         rh = daily_min_max.iloc[i].get("Chichawa_M_IHr_(%)")
    #         T = daily_min_max.iloc[i].get("Chichawa_M_ITair_(°C)")
    #         ivv = daily_min_max.iloc[i].get("Chichawa_M_IVv_(m/s)")
    #         p = daily_min_max.iloc[i].get("Chichawa_P_IP30m_(mm)")
    #         irg = daily_min_max.iloc[i].get("Chichawa_M_IRg_(W/m2)")
    #         T_min.append(T.get('min'))
    #         T_max.append(T.get('max'))
    #         pre.append(p.get('min'))
    #         et0_simple = et0_pm_simple(i, 509, 2, 31.4269444, T.get('mean'), T.get('min'), T.get('max'), ivv.get('mean'), rh.get('mean'), rh.get('min'), rh.get('max'), irg.get('mean'))
    #         et0_.append(et0_simple)
    #         dates.append(pd.Timestamp(daily_min_max.index[i]))

    # else : 

    alt = get_elevation_open(lat, long)
    # rh, irg = [], []
    # current_date = start_date_
    # while current_date <= end_date_:
        
    #     _len = 0

    #     if current_date.strftime("%Y-%m-%d") in T :
    #         _len = len(T[current_date.strftime("%Y-%m-%d")])
        
    #         if _len < 5:
    #             T_max.append(np.nan)
    #             T_min.append(np.nan)
    #             pre.append(np.nan)
    #             et0_.append(np.nan)
    #             dates.append(current_date)

    #         else :
    #             i = 0
    #             while(i < _len):
            
    #                 if T[current_date.strftime("%Y-%m-%d")][i] == np.nan or Tdew[current_date.strftime("%Y-%m-%d")][i] == np.nan:
    #                     rh.append(np.nan)
    #                 else :
    #                     rh.append(calculate_relative_humidity(T[current_date.strftime("%Y-%m-%d")][i], Tdew[current_date.strftime("%Y-%m-%d")][i]))
    #                 i += 1

    #             irg = Solar_radiation_cloudiness(34.33597054747763, current_date.timetuple().tm_yday, np.nanmean(Visibility[current_date.strftime("%Y-%m-%d")]))
    #             et0_simple = et0_pm_simple(current_date.timetuple().tm_yday, alt, 2, 34.33597054747763, np.nanmean(T[current_date.strftime('%Y-%m-%d')]), min(T[current_date.strftime('%Y-%m-%d')]), max(T[current_date.strftime('%Y-%m-%d')]), np.nanmean(Ws[current_date.strftime("%Y-%m-%d")]), np.nanmean(rh), min(rh), max(rh), irg)
    #             et0_.append(et0_simple)
    #             T_max.append(max(T[current_date.strftime("%Y-%m-%d")]))
    #             T_min.append(min(T[current_date.strftime("%Y-%m-%d")]))
    #             pre.append(np.nanmean(Rain[current_date.strftime('%Y-%m-%d')]))
    #             dates.append(current_date)
    #     current_date += timedelta(days=1)

    # end_date_ = dates[-1]

    # start_date_ = datetime.strptime(start_date, '%Y-%m-%d')
    # end_date_ = datetime.strptime(end_date, '%Y-%m-%d')
    current_date = start_date_
    et0_, T_min, T_max, pre, dates = [], [], [], [], []
    # 
    while current_date <= end_date_:
    # 
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
    # 
        # print(T_min)
        # print(T_max)
    # print(pre)
    # print(et0_)
    data = pd.DataFrame({'MinTemp' : T_min,
            'MaxTemp' : T_max,
            'Precipitation' : pre,
            'ReferenceET' : et0_,
            'Date' : dates,
        })
    
    model_os = AquaCropModel(
            sim_start_time=start_date_.strftime('%Y/%m/%d'),
            sim_end_time=end_date_.strftime('%Y/%m/%d'),
            weather_df=data,
            soil=Soil(soil_type='SandyLoam'),
            crop=Crop('Maize', planting_date=start_date_.strftime('%m/%d')),
            irrigation_management=IrrigationManagement(irrigation_method=4),
            initial_water_content=InitialWaterContent(value=['FC']),
        )

    model_os.run_model(till_termination=True)
    Water_flux = model_os.get_water_flux()[['IrrDay', 'Tr', 'DeepPerc', 'Es']]
    water_storage = model_os.get_water_storage()[['th1', 'th2', 'th3']]
    crop_growth = model_os.get_crop_growth()[['gdd_cum', 'canopy_cover', 'biomass', 'z_root', 'DryYield', 'FreshYield', 'harvest_index']]
    date_strings = [date.strftime('%Y-%m-%d') for date in dates]

    return {
        'dates' : date_strings,
        'IrrDay' : Water_flux.IrrDay.values,
        'Tr' : Water_flux.Tr.values,
        'DeepPerc' : Water_flux.DeepPerc.values,
        'Es' : Water_flux.Es.values,
        'Th1' : water_storage.th1.values,
        'Th2' : water_storage.th2.values,
        'th3' : water_storage.th3.values,
        'gdd_cum' : crop_growth.gdd_cum.values,
        'canopy_cover' : crop_growth.canopy_cover.values,
        'biomass' : crop_growth.biomass.values,
        'z_root' : crop_growth.z_root.values,
        'DryYield' : crop_growth.DryYield.values,
        'FreshYield' : crop_growth.FreshYield.values,
        'harvest_index' : crop_growth.harvest_index.values,
        'ET' : Water_flux.Tr.values + Water_flux.Es.values,
    }

# if __name__ == '__main__':
#     stations_ids = Ogimet.get_closest_stations(34.33597054747763, -4.885676122165933)
#     result = Ogimet.download(stations_ids, '2018-01-01', '2018-05-31')
#     T, Ws, Tdew, Rain, Visibility = Ogimet.decode_data_for_aquacrop()
#     result = aquacrop_run(34.33597054747763, -4.885676122165933, T, Ws, Tdew, Rain, Visibility, datetime.strptime('2018-01-01', '%Y-%m-%d'), datetime.strptime('2018-05-31', '%Y-%m-%d'))
    # print(result)