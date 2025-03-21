from  datetime import datetime, timedelta
import rasterio
import numpy as np
from aquacrop import AquaCropModel, Soil, Crop, InitialWaterContent, IrrigationManagement
import math
from .meteo_ET0 import et0_pm, et0_pm_simple
import pandas as pd
import os

def rh_calculation(T, Tdew):

    T = np.array(T, dtype=float)
    Tdew = np.array(Tdew, dtype=float)

    e_T = 6.112 * np.exp((17.67 * T) / (T + 243.5))
    # Calculate saturation vapor pressure at Tdew
    e_Tdew = 6.112 * np.exp((17.67 * Tdew) / (Tdew + 243.5))
    # Calculate relative humidity
    RH = (e_Tdew / e_T) * 100   
    return RH.tolist()

def T_collect(path):
    
    T = []

    for hour in range(24):
        hour_string = f"{hour:02d}"
        with rasterio.open(f"{path}/t2m/{hour_string}.tif") as t2m:
            
            t2m = t2m.read(1).astype('float64')

            T.append(t2m.mean() - 273.15)
    return T

def calculate_surface_solar_radiation(path):
    
    hour = 1
    irg = []
    while hour < 24:
        hour_string = f"{hour:02d}"
        hour_before = f"{hour - 1:02d}"
        with rasterio.open(f"{path}/ssrd/{hour_string}.tif") as ssrd1, \
            rasterio.open(f"{path}/ssrd/{hour_before}.tif") as ssrd2:

            ssrd1 = ssrd1.read(1).astype('float64')
            ssrd2 = ssrd2.read(1).astype('float64')
            irg.append((ssrd1.mean() - ssrd2.mean()) / 3600)
        hour += 1
    return irg

def Ws_Calulation(path):

    Ws = []
    for hour in range(24):
        hour_string = f"{hour:02d}"
        with rasterio.open(f"{path}/v_w/{hour_string}.tif") as v_w, \
            rasterio.open(f"{path}/u_w/{hour_string}.tif") as u_w :
            
            u_w = u_w.read(1).astype('float64')
            v_w = v_w.read(1).astype('float64')

            u_w[u_w == 9999] = np.nan
            v_w[v_w == 9999] = np.nan

            wind_speed = np.sqrt(u_w**2 + v_w**2)

            Ws.append(np.nanmean(wind_speed))
    return Ws

def pre_collect(path):
    Pre  = []

    for hour in range(24):
        hour_string = f"{hour:02d}"

        if os.path.exists(f"{path}/pre/{hour_string}.tif"):

            with rasterio.open(f"{path}/pre/{hour_string}.tif") as pre:

                pre = pre.read(1).astype('float64')

                pre[pre == 9999] = np.nan
                pre[pre == -9999] = np.nan
                Pre.append(pre.mean())

    return np.nanmean(Pre)    

def DT2m_collect(path):

    dT2m = []
    for hour in range(24):

        hour_string = f"{hour:02d}"
        with rasterio.open(f"{path}/dt2m/{hour_string}.tif") as Dt2m:
            
            Dt2m = Dt2m.read(1).astype('float64')

            dT2m.append(Dt2m.mean() - 273.15)
    return dT2m

def aquacrop_():

    start_date = '2022-02-01'
    end_date = '2022-05-01'

    base_dir = f"/home/hamza-boukili/Desktop/Chichaoua_olivier/"

    start_date_ = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_ = datetime.strptime(end_date, '%Y-%m-%d')

    current_date = start_date_
    lat = 31.665358
    long = -7.677980
    alt = 398
    T_min = []
    T_max = []
    et0_ = []
    pre = []
    rh = []
    rn=rs=n=ea=-9999
    h = 2
    albedo=0.23
    interior = 1
    dates = []


    while current_date <= end_date_:

        path = f"{base_dir}{current_date.strftime('%Y-%m-%d')}"
        T = T_collect(path)
        DT2m = DT2m_collect(path)
        Rh = rh_calculation(T, DT2m)
        irg = np.nanmean(calculate_surface_solar_radiation(path))
        Ws = Ws_Calulation(path)
        et0_simple = et0_pm_simple(current_date.timetuple().tm_yday, alt, 2, lat, np.nanmean(T), min(T), max(T), np.nanmean(Ws), np.nanmean(rh), min(Rh), max(Rh), irg)
        et0_.append(et0_simple)
        T_max.append(max(T))
        T_min.append(min(T))
        pre.append(pre_collect(path))
        dates.append(current_date)
        current_date += timedelta(days=1)

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
