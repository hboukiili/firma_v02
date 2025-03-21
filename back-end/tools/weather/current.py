import requests

# Define your location
lat = 34.020882  # Example latitude
long = -6.84165  # Example longitude

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": lat,
    "longitude": long,
    "current_weather": True,
    "timezone": "Africa/Casablanca",
    # Request additional variables
    "temperature_unit": "celsius",  # Options: celsius, fahrenheit
    "windspeed_unit": "ms",        # Options: kmh, ms, mph, kn
    "precipitation_unit": "mm",     # Options: mm, inch
}

# Send the request to the Open-Meteo API
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    current_weather = data.get("current_weather", {})
    print("Current Weather Data:", current_weather)
else:
    print(f"Failed to retrieve data: {response.status_code}")
