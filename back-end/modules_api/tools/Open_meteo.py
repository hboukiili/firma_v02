import requests
import numpy as np
import math
from scipy.interpolate import interp1d

def convert_wind_speed(wind_speed_10m):
    """
    Convert wind speed from 10m height to 2m height using a logarithmic wind profile.
    """
    if wind_speed_10m is None:
        return None
    return wind_speed_10m * (math.log(2 / 0.0002) / (math.log(10 / 0.0002)))

def calculate_vapor_pressure_dew_point(T_dew):
    """
    Calculate vapor pressure from dew point temperature using the Magnus-Tetens formula.
    """
    if T_dew is None:
        return np.nan
    return 6.11 * 10**((7.5 * T_dew) / (T_dew + 237.3))

def fill_missing_values(data, method='mean'):
    """
    Fill missing values in a list using averages or interpolation.
    """
    if not data:
        return data

    # Convert None to NaN for easier handling
    data = np.array(data, dtype=float)
    mask = np.isnan(data)

    if method == 'mean':
        # Fill missing values with the mean of available data
        mean_value = np.nanmean(data)
        data[mask] = mean_value
    elif method == 'interpolate':
        # Interpolate missing values
        x = np.arange(len(data))
        interp_fn = interp1d(x[~mask], data[~mask], kind='linear', fill_value="extrapolate")
        data[mask] = interp_fn(x[mask])

    return data.tolist()

def get_final_date(response):
    """
    Extract and process weather data from the Open-Meteo API response.
    """
    data = response.json()
    daily_data = data.get('daily', {})
    hourly_data = data.get('hourly', {})

    # Extract daily data
    rain_sum = daily_data.get('rain_sum', [])
    shortwave_radiation_sum = daily_data.get('shortwave_radiation_sum', [])
    et0_evapotranspiration = daily_data.get('et0_fao_evapotranspiration', [])
    temperature_max = daily_data.get('temperature_2m_max', [])
    temperature_min = daily_data.get('temperature_2m_min', [])
    rh_max = daily_data.get('relative_humidity_2m_max', [])
    rh_min = daily_data.get('relative_humidity_2m_min', [])
    wind_speed_max = daily_data.get('wind_speed_10m_max', [])

    # Extract and process hourly dew point data
    tdew = np.array(hourly_data.get('dewpoint_2m', []), dtype=float)
    Tdew = []
    Vapr = []
    for i in range(0, len(tdew), 24):
        daily_mean = np.nanmean(tdew[i:i + 24])  # Average hourly dew point for each day
        Tdew.append(daily_mean)
        Vapr.append(calculate_vapor_pressure_dew_point(daily_mean))
    return {
        "Srad": shortwave_radiation_sum,
        "Tmax": temperature_max,
        "Tmin": temperature_min,
        "Vapr": Vapr,
        "Tdew": Tdew,
        "RHmax": rh_max,
        "RHmin": rh_min,
        "Rain": rain_sum,
        "ETref": et0_evapotranspiration,
        "Wndsp": [convert_wind_speed(ws) for ws in wind_speed_max],
        "MorP": ["M"] * (len(rain_sum) + 7),
    }, daily_data.get('time')

def fao_Open_meteo(forecast, start_date, end_date, lat, long, timezone="Africa/Casablanca"):
    """
    Fetch historical weather data from Open-Meteo and combine it with forecast data.
    Fill all missing historical data with forecasted data, and use a fallback mechanism for any remaining missing values.
    """
    url                     = "https://archive-api.open-meteo.com/v1/archive"
    historic_forecast_url   = "https://historical-forecast-api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": long,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "rain_sum,shortwave_radiation_sum,et0_fao_evapotranspiration,temperature_2m_max,temperature_2m_min,relative_humidity_2m_max,relative_humidity_2m_min,wind_speed_10m_max",
        "hourly": "dewpoint_2m",
        "windspeed_unit": "ms",        # kmh, ms, mph, kn
        "timezone": timezone
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data, dates = get_final_date(response)
        daily_keys = [
            "Srad",
            "Tmax",
            "Tmin",
            "Vapr",
            "Tdew",
            "RHmax",
            "RHmin",
            "Rain",
            'ETref',
            'Wndsp'
        ]
        

        missing_indices_per_variable = {
            key: [idx for idx, value in enumerate(data[key]) if value is None]
            for key in daily_keys
        }

        if missing_indices_per_variable:
            response = requests.get(historic_forecast_url, params=params)
            response.raise_for_status()
            forecast_data, dates = get_final_date(response)

        for key, missing_indices in missing_indices_per_variable.items():
            if missing_indices_per_variable[key]:
                for idx in missing_indices:
                    data[key][idx] = forecast_data[key][idx]
            data[key] += forecast[key]
        return data
    else:
        print(f"Error: {response.status_code}")
        return None

def forcast_fao_Open_meteo(lat, long, timezone="Africa/Casablanca"):
    """
    Fetch forecast weather data from Open-Meteo.
    If forecasted data is missing, fill missing values with averages or interpolation.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "forecast_days": "7",
        "daily": "rain_sum,shortwave_radiation_sum,et0_fao_evapotranspiration,temperature_2m_max,temperature_2m_min,relative_humidity_2m_max,relative_humidity_2m_min,wind_speed_10m_max,wind_direction_10m_dominant",
        "hourly": "dewpoint_2m",
        "timezone": timezone,
        "windspeed_unit": "ms",        # kmh, ms, mph, kn
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data, dates = get_final_date(response)
        # for key in data:
        #     if key == 'MorP': continue
        #     data[key] = fill_missing_values(data[key], method='mean')  # or 'interpolate'

        return data, dates
    else:
        print(f"Error: {response.status_code}")
        return None