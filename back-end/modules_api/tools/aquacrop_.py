from aquacrop import AquaCropModel, Soil, Crop, InitialWaterContent, IrrigationManagement
from aquacrop.utils import prepare_weather, get_filepath
import pandas as pd
from .meteo_ET0 import et0_pm, et0_pm_simple
import numpy as np
import os
# from ogimet import Ogimet_class/
from  datetime import datetime, timedelta
import math

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

def aquacrop_run():

    fichier = "/app/tools/aquacrop_test/chichaoua_Zoubair_2019-2023_N0_Unification.xlsx"

    df = pd.read_excel(fichier)

    df['Date'] = pd.to_datetime(df['Date'])

    # Group by date and apply min and max aggregation functions
    daily_min_max = df.groupby(df['Date'].dt.date).agg({
        'Chichawa_M_IDv_(°)': ['min', 'max'],
        'Chichawa_M_IHr_(%)': ['min', 'max', 'mean'],
        'Chichawa_M_IRg_(W/m2)': ['mean'],
        'Chichawa_M_ITair_(°C)': ['min', 'max', 'mean'],
        'Chichawa_M_IVv_(m/s)': ['min', 'max', 'mean'],
        'Chichawa_P_IP30m_(mm)': ['min', 'max']
    })


    h = 2
    interior = 1
    albedo=0.23
    rn=rs=n=ea=-9999
    T_min = []
    T_max = []
    et0_ = []
    pre = []
    dates = []

    for i in range(0, 121):

        rh = daily_min_max.iloc[i].get("Chichawa_M_IHr_(%)")
        T = daily_min_max.iloc[i].get("Chichawa_M_ITair_(°C)")
        ivv = daily_min_max.iloc[i].get("Chichawa_M_IVv_(m/s)")
        p = daily_min_max.iloc[i].get("Chichawa_P_IP30m_(mm)")
        irg = daily_min_max.iloc[i].get("Chichawa_M_IRg_(W/m2)")
        # print(rh, T, ivv, p, irg)
        T_min.append(T.get('min'))
        T_max.append(T.get('max'))
        pre.append(p.get('min'))
        et0_simple = et0_pm_simple(i, 509, 2, 31.4269444, T.get('mean'), T.get('min'), T.get('max'), ivv.get('mean'), rh.get('mean'), rh.get('min'), rh.get('max'), irg.get('mean'))
        et0_.append(et0_simple)
        dates.append(pd.Timestamp(daily_min_max.index[i]))

    data = pd.DataFrame({'MinTemp' : T_min,
            'MaxTemp' : T_max,
            'Precipitation' : pre,
            'ReferenceET' : et0_,
            'Date' : dates,
        })
    
    model_os = AquaCropModel(
            sim_start_time=f"{2019}/01/01",
            sim_end_time=f"{2019}/05/01",
            weather_df=data,
            soil=Soil(soil_type='SandyLoam'),
            crop=Crop('Maize', planting_date='01/01'),
            irrigation_management=IrrigationManagement(irrigation_method=4),
            initial_water_content=InitialWaterContent(value=['FC']),
        )

    model_os.run_model(till_termination=True)
    Water_flux = model_os.get_water_flux()[['IrrDay', 'Tr', 'DeepPerc', 'Es']]
    water_storage = model_os.get_water_storage()[['th1', 'th2', 'th3']]
    crop_growth = model_os.get_crop_growth()[['gdd_cum', 'canopy_cover', 'biomass', 'z_root', 'DryYield', 'FreshYield', 'harvest_index']]
    date_strings = [date.strftime('%Y-%m-%d') for date in dates]

    print(Water_flux.IrrDay.values)
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
