import requests
import datetime

class WeatherFetcher:
    def __init__(self, url):
        self.url = url

    def fetch_weather_data(self, station_id, date_begin, date_end):
        # Convert date formats
        date_begin_format = datetime.datetime.strptime(date_begin, '%Y-%m-%d').strftime('%Y%m%d%H%M')
        date_end_format = datetime.datetime.strptime(date_end, '%Y-%m-%d').strftime('%Y%m%d%H%M')
        
        # Parameters as a dictionary
        params = {
            'block': station_id,
            'begin': date_begin_format,
            'end': date_end_format
        }
        
        # Send the GET request
        response = requests.get(self.url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.text
        else:
            return f"Error: {response.status_code} - {response.reason}"

# Example usage
url = "http://www.ogimet.com/cgi-bin/getsynop"
weather_fetcher = WeatherFetcher(url)
print(weather_fetcher.fetch_weather_data('60115', '2018-01-30', '2018-02-10'))
