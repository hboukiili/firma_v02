import  metno_locationforecast as metno
import numpy as np
import pandas as pd

pd.set_option('display.max_rows', None)  # This will display all rows
pd.set_option('display.max_columns', None)  # This will display all columns

place = metno.Place("Myplace", 32.2355, -7.9533)
forecast = metno.Forecast(place, "hamza.boukili@um6p.ma")
forecast.forecast_type='complete'
forecast.update()
table = np.zeros((len(forecast.data.intervals)-1,8))
table_dates = []
for i in range(len(forecast.data.intervals)-1):
    interval = forecast.data.intervals[i]

    table_dates.append(interval.start_time)

    table[i,0] = interval.variables["air_temperature"].value
    table[i,1]  = interval.variables["wind_from_direction"].value
    table[i,2]  = interval.variables["relative_humidity"].value
    table[i,3]  = interval.variables["air_pressure_at_sea_level"].value
    table[i,4]  = interval.variables["wind_speed"].value
    table[i,5]  = interval.variables["precipitation_amount"].value
    table[i,6]  = interval.variables["dew_point_temperature"].value
    table[i,7]  = interval.variables["cloud_area_fraction"].value

for i in range(len(forecast.data.intervals)-1):
    print(table_dates[i], table[i])

# for interval in forecast.data.intervals:
#     # Extract all the required variables and append to the data list
#     entry = {
#         "Start Time": interval.start_time,
#         "Air Temperature": interval.variables["air_temperature"].value,
#         "Wind Direction": interval.variables["wind_from_direction"].value,
#         "Relative Humidity": interval.variables["relative_humidity"].value,
#         "Air Pressure": interval.variables["air_pressure_at_sea_level"].value,
#         "Wind Speed": interval.variables["wind_speed"].value,
#         # "Precipitation Amount": interval.variables["precipitation_amount"].value,
#         "Dew Point Temperature": interval.variables["dew_point_temperature"].value,
#         "Cloud Area Fraction": interval.variables["cloud_area_fraction"].value
#     }

