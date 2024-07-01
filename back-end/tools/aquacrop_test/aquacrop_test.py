from aquacrop import AquaCropModel, Soil, Crop, InitialWaterContent
from aquacrop.utils import prepare_weather, get_filepath
import pandas as pd
from meteo_ET0 import et0_pm, et0_pm_simple
import numpy as np
import os
from ogimet import Ogimet_class
from  datetime import datetime, timedelta
import math

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






Ogimet = Ogimet_class()

start_date = '2018-01-01'
end_date = '2018-01-31'
print("starting...")
data = Ogimet.download( ["60115", "60115"], start_date, end_date)
print('got Data ...')
T, Ws, Tdew, Rain = Ogimet.decode_data()
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
irg = 132.47606058304277
while current_date <= end_date_:

    i = 0
    while(i < len(T[current_date.strftime("%Y-%m-%d")])):
        rh.append(calculate_relative_humidity(T[current_date.strftime("%Y-%m-%d")][i], Tdew[current_date.strftime("%Y-%m-%d")][i])) 
        i += 1
    # print(rh)
    # break 
    print(min(rh), max(rh))

    # et0_simple = et0_pm_simple(current_date.timetuple().tm_yday, 509, 2, 34.33597054747763, np.nanmean(T[current_date.strftime('%Y-%m-%d')]), min(T[current_date.strftime('%Y-%m-%d')]), max(T[current_date.strftime('%Y-%m-%d')]), np.nanmean(Ws[current_date.strftime("%Y-%m-%d")]), np.nanmean(rh), min(rh), max(rh), irg)
    # print(et0_simple)
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


# data = pd.DataFrame({'MinTemp' : T_min,
#         'MaxTemp' : T_max,
#         'Precipitation' : pre,
#         'ReferenceET' : et0_,
#         'Date' : dates,
#     })

# model_os = AquaCropModel(
#             sim_start_time=f"{2019}/01/01",
#             sim_end_time=f"{2019}/05/01",
#             weather_df=data,
#             soil=Soil(soil_type='SandyLoam'),
#             crop=Crop('Maize', planting_date='01/01'),
#             # irrigation_management=
#             initial_water_content=InitialWaterContent(value=['FC']),
#         )


# model_os.run_model(till_termination=True)
# # model_os.run_model(num_steps=30, till_termination=True, initialize_model=True, process_outputs=True)

# Water_flux = model_os.get_water_flux()[['IrrDay', 'Tr', 'DeepPerc', 'Es']]
# water_storage = model_os.get_water_storage()[['th1', 'th2', 'th3']]
# crop_growth = model_os.get_crop_growth()[['gdd_cum', 'canopy_cover', 'biomass', 'z_root', 'DryYield', 'FreshYield', 'harvest_index']]

# print(model_os.get_crop_growth())
# print(model_os.get_water_storage())
# print(model_os.get_simulation_results())

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
