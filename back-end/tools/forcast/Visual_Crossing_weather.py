import requests

API_key = "8XMTJSYYT4VHSQ7K6QXCSRE7V"
lat = "32.2355"
lon = "-7.9533"
start_date = "2018-09-01"
end_date = "2018-09-05"

url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{lon}/{start_date}/{end_date}?key={API_key}"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print(data)
    for day in data['days']:
        # Displaying the daily summary
        print(f"Date: {day['datetime']}")
        print(f"  Temperature (Max/Min/Avg): {day['tempmax']}°C / {day['tempmin']}°C / {day['temp']}°C")
        print(f"  Humidity: {day['humidity']}%")
        print(f"  Precipitation: {day['precip']} mm")
        print(f"  Cloud Cover: {day['cloudcover']}%")
        print(f"  Conditions: {day['conditions']}")
        print(f"  Stations: {', '.join(day['stations']) if 'stations' in day else 'N/A'}")
        print("\n  Hourly Data:")
        
        # Displaying hourly data for the day
        for hour in day['hours']:
            print(f"    {hour['datetime']}:")
            print(f"      Temp: {hour['temp']}°C, Feels Like: {hour['feelslike']}°C")
            print(f"      Humidity: {hour['humidity']}%")
            print(f"      Wind Speed: {hour['windspeed']} km/h, Wind Gust: {hour['windgust']} km/h")
            print(f"      Cloud Cover: {hour['cloudcover']}%, UV Index: {hour['uvindex']}")
            print("")
else:
    print(f"Error: {response.status_code}")
