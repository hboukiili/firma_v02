import pyfao56 as fao
from pyfao56.tools import forecast
import numpy as np
import pandas as pd

# self.wdata = pd.DataFrame(data, index=index)
# self.idata = pd.DataFrame(data, index=index)


weather_data = {
    "Srad": [11.43, 13.09, 13.04, 13.04, 12.87, 12.46, 9.73, 12.22, 12.59, 12.49] * 30,
    "Tmax": [12.4, 16.3, 16.7, 15.5, 17.1, 20.7, 17.6, 19.1, 18.5, 19.6, ] * 30,
    "Tmin": [-3.1, 1.1, 0.2, -0.7, -3.1, 0.9, -0.2, 0.5, 1.2, -1.0] * 30,
    "Vapr": [np.nan] * 300,
    "Tdew": [-2.5, -4.9, -5.3, -3.5, -3.7, 0.1, 1.2, 1.1, -0.8, 0.0] * 30,
    "RHmax": [92.2, 75.9, 68.6, 75.1, 87.4, 89.5, 88.0, 95.9, 84.7, 93.2] * 30,
    "RHmin": [27.3, 20.5, 19.2, 25.9, 23.1, 20.5, 29.9, 23.3, 20.9, 23.7] * 30,
    "Wndsp": [1.2, 2.1, 2.4, 1.4, 0.9, 1.4, 0.8, 1.4, 1.1, 1.0] * 30,
    "Rain": [0.25, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00] * 30,
    "ETref": [1.36, 2.27, 2.56, 1.73, 1.47, 2.03, 1.31, 1.88, 1.67, 1.62] * 30,
    "MorP": ["M"] * 300
}

irr_data = {
    'Depth': [33.0, 108.0, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 16.2, 10.1, 10.1, 10.1,
              10.1, 10.1, 10.1, 10.1, 10.1, 10.1, 10.1, 20.3, 10.1, 10.1, 10.1, 20.3, 20.3, 10.1, 10.1, 10.1, 10.1, 10.1, 10.1, 10.1,
              10.1, 4.1, 12.2, 12.2, 12.2, 12.2, 4.1, 10.1, 10.1, 10.1],
    'fw': [0.5, 0.5, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 
           0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2,
           0.2, 0.2],
    'ieff': [100.0] * 50
}

start_date = "2013-01-01"
end_date = "2013-12-31"
date_range = pd.date_range(start=start_date, end=end_date, freq='D')
index = date_range.strftime('%Y-%j')

index = index[:300]

par = fao.Parameters()

wth = fao.Weather(weather_data, index)

irr = fao.Irrigation(irr_data, index)

mdl = fao.Model('2013-113','2013-200', par, wth, irr=irr)

mdl.run()

print(mdl)


# Define the start date and end date
# start_date = "2013-01-01"
# end_date = "2013-12-31"

# # Generate the date range
# date_range = pd.date_range(start=start_date, end=end_date, freq='D')

# # Format the date range to match the required index format
# index = date_range.strftime('%Y-%j')

# # Use only the first 10 entries for the index to match the data length
# index = index[:10]

# # Create the DataFrame
# df = pd.DataFrame(data, index=index)

# Display the DataFrame
# print(df)

# index = index[:50]
# self.idata = pd.DataFrame(data, index=index)