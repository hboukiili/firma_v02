import requests
import time

lat = "32.2355"
lon = "-7.9533"
API_key = "85461dddb7698ac03b2bf4c5b22f5369"
url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric"  # Added units=metric for Celsius


response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Convert the response to JSON
    print(data)  # Print the weather data
else:
    print(f"Error: {response.status_code}")

print("history ...")

start_date = "2018-01-01"
end_date = "2018-05-01"

# Convert start and end dates to Unix timestamps
start_timestamp = int(time.mktime(time.strptime(start_date, "%Y-%m-%d")))
end_timestamp = int(time.mktime(time.strptime(end_date, "%Y-%m-%d")))

# hourly 4 days
# url = f"https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}&lon={lon}&appid={API_key}"

# 16 days
url = f"https://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt=7&appid={API_key}"

response = requests.get(url)

# Check if the request for historical data was successful
if response.status_code == 200:
    data = response.json()  # Convert the response to JSON
    print("Historical Weather Data:", data)  # Print the historical weather data
else:
    print(f"Error fetching historical weather data: {response.status_code}")