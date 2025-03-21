import requests
import time

lat = "32.2355"
lon = "-7.9533"
API_key = "85461dddb7698ac03b2bf4c5b22f5369"
params = {
    "lat": lat,           # Latitude for Los Angeles
    "lon": lon,         # Longitude for Los Angeles
    "appid": API_key,       # Your OpenWeather API key
    "units": "metric"       # Units of measurement ('metric' for °C, 'imperial' for °F)
}

url = "https://api.openweathermap.org/data/2.5/weather"

response = requests.get(url, params=params)




# response = requests.get(url)

# # Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Convert the response to JSON
    
    # Extract weather data
    main = data.get("main", {})
    wind = data.get("wind", {})
    clouds = data.get("clouds", {})
    rain = data.get("rain", {})
    snow = data.get("snow", {})
    visibility = data.get("visibility")
    weather_desc = data.get("weather", [{}])[0].get("description")
    
    # Variables
    temperature = main.get("temp")
    feels_like = main.get("feels_like")
    humidity = main.get("humidity")
    pressure = main.get("pressure")
    wind_speed = wind.get("speed")
    wind_direction = wind.get("deg")
    cloud_cover = clouds.get("all")
    rain_volume = rain.get("1h", 0)     # Rain volume in last hour
    snow_volume = snow.get("1h", 0)     # Snow volume in last hour
    
    # Print the weather data
    print("Current Weather Data:")
    print(f"Temperature: {temperature} °C")
    print(f"Feels Like: {feels_like} °C")
    print(f"Humidity: {humidity} %")
    print(f"Pressure: {pressure} hPa")
    print(f"Wind Speed: {wind_speed} m/s")
    print(f"Wind Direction: {wind_direction}°")
    print(f"Cloud Cover: {cloud_cover} %")
    print(f"Visibility: {visibility} m")
    print(f"Rain Volume (last hour): {rain_volume} mm")
    print(f"Snow Volume (last hour): {snow_volume} mm")
    print(f"Weather Description: {weather_desc}")# else:
#     print(f"Error: {response.status_code}")

# print("history ...")

# start_date = "2018-01-01"
# end_date = "2018-05-01"

# # Convert start and end dates to Unix timestamps
# start_timestamp = int(time.mktime(time.strptime(start_date, "%Y-%m-%d")))
# end_timestamp = int(time.mktime(time.strptime(end_date, "%Y-%m-%d")))

# # hourly 4 days
# # url = f"https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}&lon={lon}&appid={API_key}"

# # 16 days
# url = f"https://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt=7&appid={API_key}"

# response = requests.get(url)

# # Check if the request for historical data was successful
# if response.status_code == 200:
#     data = response.json()  # Convert the response to JSON
#     print("Historical Weather Data:", data)  # Print the historical weather data
# else:
#     print(f"Error fetching historical weather data: {response.status_code}")