import requests
import pandas as pd

# Define location (Fez, Morocco)
lat = 31.666682   
long = -7.679958

# Define API URL
url = "https://archive-api.open-meteo.com/v1/archive"





# Define parameters for API request
params = {
    "latitude": lat,  
    "longitude": long,  
    "start_date": "2024-11-01",  
    "end_date": "2024-12-31",  
    "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,relative_humidity_2m_max,relative_humidity_2m_min,relative_humidity_2m_mean,shortwave_radiation_sum,wind_speed_10m_max,et0_fao_evapotranspiration",
    "timezone": "auto"
}

# params = {
#     "latitude": lat,
#     "longitude": long,
#     "start_date": "2000-01-01",
#     "end_date": "2024-12-31",
#     "hourly": "temperature_2m,relativehumidity_2m,shortwave_radiation,windspeed_10m,et0_fao_evapotranspiration,dewpoint_2m",
#     "timezone": "auto"
# }

try:
    # Make API request
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an error if the request fails
    
#     # Convert response to JSON
    data = response.json()
    
#     # Extract weather variables from hourly data (the "time" field includes date and hour)
    dates = data['daily']['time']
    ta_max = data['daily'].get('temperature_2m_max', [])
    ta_min = data['daily'].get('temperature_2m_min', [])
    ta_mean = data['daily'].get('temperature_2m_mean', [])
    rh_max = data['daily'].get('relative_humidity_2m_max', [])
    rh_min = data['daily'].get('relative_humidity_2m_min', [])
    rh_mean = data['daily'].get('relative_humidity_2m_mean', [])
    rs_mean = data['daily'].get('shortwave_radiation_sum', [])
    wind_10m = data['daily'].get('wind_speed_10m_max', [])

    et0_pm = data['daily'].get('et0_fao_evapotranspiration', [])

   
    print(et0_pm)

    payload = {
        "ta_max": ta_max,     # e.g., [30.5, 31.0, 29.8, ...]
        "rh_mean": rh_mean,   # e.g., [65, 70, 68, ...]
        "rs_mean": rs_mean    # e.g., [15.2, 14.8, 16.0, ...]
    }

    response = requests.post('http://localhost:8001/predict_cb/', json=payload)
    data = response.json()
    print(data)
#     # Create a DataFrame
#     weather_df = pd.DataFrame({
#         'datetime': dates,
#         'temperature_2m': temperature,
#         'relativehumidity_2m': relative_humidity,
#         'shortwave_radiation': shortwave_radiation,
#         'windspeed_10m': wind_speed,
#         'et0_fao_evapotranspiration': et0,
#         'dewpoint_2m': dewpoint
#     })
    
#     # Convert the datetime column to a proper datetime format (including hours)
#     weather_df['datetime'] = pd.to_datetime(weather_df['datetime'])
    
#     # Save to CSV
#     weather_df.to_csv('weather_data_hourly.csv', index=False)
    
#     print("✅ Hourly weather data saved as weather_data_hourly.csv")


except requests.exceptions.RequestException as e:
    print("❌ Error fetching data:", e)
