import requests

API_key = "9500c41a2fb04752ad5193733241809"
lat = "32.2355"
lon = "-7.9533"
start_date = "2023-09-01"  # YYYY-MM-DD format
end_date = "2023-09-05"

# Loop through the date range
current_date = start_date
# url = f"https://api.weatherapi.com/v1/history.json?key={API_key}&q={lat},{lon}&dt={current_date}"

url = f"http://api.weatherapi.com/v1/history.json?key={API_key}&q={lat},{lon}&dt=2024-01-01"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")
