from aquacrop import AquaCropModel, Soil, Crop, InitialWaterContent
from aquacrop.utils import prepare_weather, get_filepath
import pandas as pd
from meteo_ET0 import et0_pm, et0_pm_simple
import numpy as np
import os
from ogimet import Ogimet_class
from  datetime import datetime, timedelta
import math
from math import *
import urllib
import requests
import simplejson as json


pd.set_option('display.max_rows', None)  # This will display all rows
pd.set_option('display.max_columns', None)  # This will display all columns

def calculate_relative_humidity(T, Tdew):
    # Calculate saturation vapor pressure at T

    e_T = 6.112 * math.exp((17.67 * T) / (T + 243.5))
    # Calculate saturation vapor pressure at Tdew
    e_Tdew = 6.112 * math.exp((17.67 * Tdew) / (Tdew + 243.5))
    # Calculate relative humidity
    RH = (e_Tdew / e_T) * 100
    return RH

def Extraterrestrial_radiation(lat,jday):
	lat_rad=lat*pi/180.
	dr=1 + 0.033 * cos(2*pi/365*jday)
	soldecl=0.409*sin((2*pi/365*jday) - 1.39)
	sunset_angle=acos(-tan(lat_rad)*tan(soldecl))
	   
	ra= (24*60/pi)* 0.082 * dr * (sunset_angle * sin(lat_rad) * sin(soldecl) + cos(lat_rad) * cos(soldecl) * sin(sunset_angle))

	return(ra)

def Solar_radiation_cloudiness(lat,jday,cF):

    const_as = 0.25
    const_bs = 0.5
    ra = Extraterrestrial_radiation(lat,jday)
    # print('ra = ', ra, '...', jday)
    rs = (const_as+const_bs*cF/100.)*ra
    # print(rs)
    return(rs)

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

# def mapquest_elevation(lat,lon):
   
#     url="http://open.mapquestapi.com/elevation/v1/profile?key=Fmjtd|luurn10720%2Ca0%3Do5-9wy05f&shapeFormat=raw&latLngCollection="+str(lat)+","+str(lon)
    
#     opener = urllib.request.build_opener()
#     urllib.request.install_opener(opener)
#     f = opener.open(url)
#     json_string = f.read()
#     parsed_json = json.loads(json_string)
#     masl=float(parsed_json['elevationProfile'][0]['height'])
#     return(masl)



Ogimet = Ogimet_class()

start_date = '2018-01-01'
end_date = '2018-05-01'
print("starting...")
data = Ogimet.download( ["60156", "60115"], start_date, end_date)
print('got Data ...')
T, Ws, Tdew, Rain, Visibility = Ogimet.decode_data()
print(T)
print(Ws)
print(Tdew)
print(Rain)
print(Visibility)
print("Done decoding Data ...")

start_date_ = datetime.strptime(start_date, '%Y-%m-%d')
end_date_ = datetime.strptime(end_date, '%Y-%m-%d')

current_date = start_date_
h = 2
interior = 1
albedo=0.23
rn=rs=n=ea=-9999
T_min = []
T_max = []
et0_ = []
pre = []
dates = []
rh = []
x = 0
# irg = []
alt = 398
while current_date <= end_date_:
    _len = len(T[current_date.strftime("%Y-%m-%d")])
    
    if _len < 5:
        T_max.append(np.nan)
        T_min.append(np.nan)
        pre.append(np.nan)
        et0_.append(np.nan)
        dates.append(current_date)

    else :
        i = 0
        while(i < _len):
    
            if T[current_date.strftime("%Y-%m-%d")][i] == np.nan or Tdew[current_date.strftime("%Y-%m-%d")][i] == np.nan:
                rh.append(np.nan)
            else :
                rh.append(calculate_relative_humidity(T[current_date.strftime("%Y-%m-%d")][i], Tdew[current_date.strftime("%Y-%m-%d")][i]))
            i += 1

        irg = Solar_radiation_cloudiness(34.33597054747763, current_date.timetuple().tm_yday, np.nanmean(Visibility[current_date.strftime("%Y-%m-%d")]))
        et0_simple = et0_pm_simple(current_date.timetuple().tm_yday, alt, 2, 34.33597054747763, np.nanmean(T[current_date.strftime('%Y-%m-%d')]), min(T[current_date.strftime('%Y-%m-%d')]), max(T[current_date.strftime('%Y-%m-%d')]), np.nanmean(Ws[current_date.strftime("%Y-%m-%d")]), np.nanmean(rh), min(rh), max(rh), irg)
        et0_.append(et0_simple)

        # print('et0 = ', et0_simple,'T ', np.nanmean(T[current_date.strftime('%Y-%m-%d')]),'T min ', min(T[current_date.strftime('%Y-%m-%d')]),'T max ',  max(T[current_date.strftime('%Y-%m-%d')]),'W ', np.nanmean(Ws[current_date.strftime("%Y-%m-%d")]),'rh min ',  min(rh),'rh max ',  max(rh),'irg ', irg)
        T_max.append(max(T[current_date.strftime("%Y-%m-%d")]))
        T_min.append(min(T[current_date.strftime("%Y-%m-%d")]))
        pre.append(np.nanmean(Rain[current_date.strftime('%Y-%m-%d')]))
        dates.append(current_date)
    current_date += timedelta(days=1)


# for i in range(0, 121):

#     rh = daily_min_max.iloc[i].get("Chichawa_M_IHr_(%)")
#     T = daily_min_max.iloc[i].get("Chichawa_M_ITair_(°C)")
#     ivv = daily_min_max.iloc[i].get("Chichawa_M_IVv_(m/s)")
#     p = daily_min_max.iloc[i].get("Chichawa_P_IP30m_(mm)")
#     irg = daily_min_max.iloc[i].get("Chichawa_M_IRg_(W/m2)")
#     # print(rh, T, ivv, p, irg)
#     T_min.append(T.get('min'))
#     T_max.append(T.get('max'))
#     pre.append(p.get('min'))
    #   et0_simple = et0_pm_simple(i, 509, 2, 31.4269444, T.get('mean'), T.get('min'), T.get('max'), ivv.get('mean'), rh.get('mean'), rh.get('min'), rh.get('max'), irg.get('mean'))
#     print(et0_simple, daily_min_max.index[i])
#     et0_.append(et0_simple)
#     dates.append(pd.Timestamp(daily_min_max.index[i]))

# print(len(T_max), len(T_min), len(pre), len(et0_), len(dates))
data = pd.DataFrame({'MinTemp' : T_min,
        'MaxTemp' : T_max,
        'Precipitation' : pre,
        'ReferenceET' : et0_,
        'Date' : dates,
    })

model_os = AquaCropModel(
            sim_start_time=f"{2018}/01/01",
            sim_end_time=f"{2018}/01/31",
            weather_df=data,
            soil=Soil(soil_type='SandyLoam'),
            crop=Crop('Maize', planting_date='01/01'),
            # irrigation_management=
            initial_water_content=InitialWaterContent(value=['FC']),
        )


model_os.run_model(till_termination=True)
# model_os.run_model(num_steps=30, till_termination=True, initialize_model=True, process_outputs=True)

Water_flux = model_os.get_water_flux()[['IrrDay', 'Tr', 'DeepPerc', 'Es']]
water_storage = model_os.get_water_storage()[['th1', 'th2', 'th3']]
crop_growth = model_os.get_crop_growth()[['gdd_cum', 'canopy_cover', 'biomass', 'z_root', 'DryYield', 'FreshYield', 'harvest_index']]

# print(model_os.get_water_flux())
# print(model_os.get_water_storage())
# print(model_os.get_crop_growth())

# hr_min = daily_min_max["Chichawa_M_IHr_(%)"].get('min')
# hr_max = daily_min_max["Chichawa_M_IHr_(%)"].get('max')
# print(hr_max)
# dates = list(df['Date'].dt.date)

# print(dates)
# print(daily_min_max['Chichawa_M_IHr_(%)'].get('min'))
# new_columns = ['{}_{}_{}'.format(col[0], col[1], col[2]) for col in existing_columns]

# print(daily_min_max.head())
# Dates = daily_min_max.index.astype(str).tolist()
# print(Dates)

# ihr = humidite relative
# irg = global radiations
# itair = temperature de l'aire
# ivv = vitess de vent
# p = pluit
