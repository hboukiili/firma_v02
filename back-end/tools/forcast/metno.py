import  metno_locationforecast as metno
import numpy as np



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