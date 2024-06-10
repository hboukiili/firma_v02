from aquacrop import AquaCropModel, Soil, Crop, InitialWaterContent
from aquacrop.utils import prepare_weather, get_filepath
import pandas as pd
from meteo_ET0 import et0_pm, et0_pm_simple
import numpy as np

weather_file_path = get_filepath('tunis_climate.txt')

# print(model_os.get_additional_information().head())
# model_results = model_os.get_simulation_results().head() = yield
# model_os.get_water_flux().head() = water budget flux *
# model_os.get_water_storage().head() = ? *
# model_os.get_crop_growth().head() = crop information *
# print(model_results)


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

fichier = "./chichaoua_Zoubair_2019-2023_N0_Unification.xlsx"

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

# print(daily_min_max)

test = daily_min_max.head()
h = 2
interior = 1
albedo=0.23
rn=rs=n=ea=-9999
T_min = []
T_max = []
et0_ = []
pre = []
dates = []
for i in range(0, 31):

    rh = daily_min_max.iloc[i].get("Chichawa_M_IHr_(%)")
    T = daily_min_max.iloc[i].get("Chichawa_M_ITair_(°C)")
    ivv = daily_min_max.iloc[i].get("Chichawa_M_IVv_(m/s)")
    p = daily_min_max.iloc[i].get("Chichawa_P_IP30m_(mm)")
    irg = daily_min_max.iloc[i].get("Chichawa_M_IRg_(W/m2)")
    # print(rh, T, ivv, p, irg)
    T_min.append(T.get('min'))
    T_max.append(T.get('max'))
    pre.append(p.get('min'))
    # et0 = et0_pm(31.4269444,i,509,rn,irg.get('mean'),n,ea,calculate_dew_point(T.get('mean'), rh.get('mean')),T.get('mean'),T.get('min'),T.get('max'),interior,rh.get('min'),rh.get('max'),rh.get('mean'),ivv.get('mean'),h,albedo, -9999)
    et0_simple = et0_pm_simple(i, 509, 2, 31.4269444, T.get('mean'), T.get('min'), T.get('max'), ivv.get('mean'), rh.get('mean'), rh.get('min'), rh.get('max'), irg.get('mean'))
    print(et0_simple, daily_min_max.index[i])
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
            sim_end_time=f"{2019}/01/30",
            weather_df=data,
            soil=Soil(soil_type='SandyLoam'),
            crop=Crop('Maize', planting_date='01/01'),
            initial_water_content=InitialWaterContent(value=['FC']),
        )

model_os.run_model(till_termination=True)

# print(model_os.get_water_flux())
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
