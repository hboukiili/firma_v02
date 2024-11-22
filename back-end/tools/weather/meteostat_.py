from datetime import datetime
from meteostat import Point, Daily, Hourly
import pandas as pd


pd.set_option('display.max_rows', None)  # This will display all rows
pd.set_option('display.max_columns', None)  # This will display all columns


# # Define the location (latitude, longitude, and elevation)
# location = Point(31.66580238055144, -7.678321344603916)  # Example: Marrakesh, Morocco

# # Set the time period
# start = datetime(2024, 1, 10)
# end = datetime(2024, 5, 31)

# # Get daily weather data for the specified location and time period
# data = Hourly(location, start, end)
# data = data.fetch()

# # Display the data
# print(data)

# import requests
# import pandas as pd

# # Define the historical data endpoint and parameters
# endpoint = "https://archive-api.open-meteo.com/v1/archive"
# parameters = {
#     "latitude": 31.66580238055144,  # Latitude for Marrakesh, Morocco
#     "longitude": -7.678321344603916,  # Longitude for Marrakesh, Morocco
#     "start_date": "2024-01-10",  # Set your desired start date
#     "end_date": "2024-05-31",    # Set your desired end date
#     "hourly": ",".join([
#         "temperature_2m", "relative_humidity_2m", "dew_point_2m",
#         "apparent_temperature", "precipitation_probability", "precipitation",
#         "rain", "showers", "snowfall", "snow_depth", "weather_code",
#         "pressure_msl", "surface_pressure", "cloudcover", "cloudcover_low",
#         "cloudcover_mid", "cloudcover_high", "visibility", "evapotranspiration",
#         "et0_fao_evapotranspiration", "vapor_pressure_deficit", "windspeed_10m",
#         "windspeed_80m", "windspeed_120m", "windspeed_180m", "winddirection_10m",
#         "winddirection_80m", "winddirection_120m", "winddirection_180m",
#         "windgusts_10m", "temperature_80m", "temperature_120m", "temperature_180m",
#         "soil_temperature_0cm", "soil_temperature_6cm", "soil_temperature_18cm",
#         "soil_temperature_54cm", "soil_moisture_0_1cm", "soil_moisture_1_3cm",
#         "soil_moisture_3_9cm", "soil_moisture_9_27cm", "soil_moisture_27_81cm"
#     ]),
#     "timezone": "auto"  # Automatically sets the timezone based on coordinates
# }

# # Make the API request
# response = requests.get(endpoint, params=parameters)

# # Check if the request was successful
# if response.status_code == 200:
#     data = response.json()
    
#     # Extract hourly data and convert it to a DataFrame
#     hourly_data = data['hourly']
#     df = pd.DataFrame(hourly_data)
    
#     # Convert the timestamp column to a datetime format if necessary
#     if 'time' in df.columns:
#         df['time'] = pd.to_datetime(df['time'])
    
#     # Display the DataFrame
#     print(df)
# else:
#     print(f"Error: {response.status_code}")

import requests
import pandas as pd

# Replace with your Visual Crossing API key
API_key = "8XMTJSYYT4VHSQ7K6QXCSRE7V"

# Define the endpoint and parameters for historical weather data
endpoint = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
latitude = 31.66580238055144
longitude = -7.678321344603916
start_date = "2024-01-10"
end_date = "2024-05-31"
parameters = {
    "unitGroup": "metric",  # Use "us" for Fahrenheit and imperial units
    "key": API_key,
    "include": "hours",     # Include hourly data
    "contentType": "json"   # Get the response in JSON format
}

# Build the request URL with coordinates
url = f"{endpoint}/{latitude},{longitude}/{start_date}/{end_date}"

# Make the API request
response = requests.get(url, params=parameters)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Extract hourly data
    hourly_data = []
    for day in data['days']:
        for hour in day['hours']:
            hourly_data.append(hour)

    # Convert to DataFrame
    df = pd.DataFrame(hourly_data)
    
    # Convert the datetime column to datetime format
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'])
    
    # Display the DataFrame
    print(df)
else:
    print(f"Error: {response.status_code}, {response.text}")
