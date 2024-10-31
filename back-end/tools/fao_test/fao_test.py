import pyfao56 as fao
from pyfao56.tools import forecast
import numpy as np
import os
from osgeo import gdal, ogr, osr
import pandas as pd
from  datetime import datetime, timedelta
import requests
from shapely.wkt import loads
import rasterio
import rasterio.mask as msk
from pyproj import Transformer
from shapely.geometry import mapping

import math


# self.wdata = pd.DataFrame(data, index=index)
# self.idata = pd.DataFrame(data, index=index)
pd.set_option('display.max_rows', None)  # This will display all rows
pd.set_option('display.max_columns', None)  # This will display all columns



def convert_wind_speed(wind_speed_10m):
    
    ws_2m = []
    for i in wind_speed_10m:
        ws_2m.append(i * (math.log(2 / 0.0002) / math.log(10 / 0.0002)) / 3600)
    return ws_2m

def calculate_vapor_pressure_dew_point(T_dew):
    return 6.11 * 10**((7.5 * T_dew) / (T_dew + 237.3))

def Open_meteo(start_date, end_date, lat, long):
    # Set the URL for the Open-Meteo API (historical data)
    url = "https://archive-api.open-meteo.com/v1/archive"

    # Define parameters for the API request
    params = {
        "latitude": lat,  # Replace with the latitude of your location
        "longitude": long,  # Replace with the longitude of your location
        "start_date": start_date,  # Start date for historical data
        "end_date": end_date,  # End date for historical data
        # "daily" : "rain_sum,shortwave_radiation_sum,et0_fao_evapotranspiration,temperature_2m_max,temperature_2m_min,relative_humidity_2m_max,relative_humidity_2m_min,wind_speed_10m_max",
        # "hourly": "dewpoint_2m",
        'current': 'temperature_2m, et0_fao_evapotranspiration',
        "timezone": "Africa/Casablanca"  # Set your timezone
    }


    # Send the request to the Open-Meteo API
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print(data)
        exit()
        daily_data = data.get('daily', {})
        rain_sum = daily_data.get('rain_sum', [])
        shortwave_radiation_sum = daily_data.get('shortwave_radiation_sum', [])
        et0_evapotranspiration = daily_data.get('et0_fao_evapotranspiration', [])
        temperature_max = daily_data.get('temperature_2m_max', [])
        temperature_min = daily_data.get('temperature_2m_min', [])
        rh_max = daily_data.get('relative_humidity_2m_max', [])
        tdew = data['hourly']['dewpoint_2m']
        rh_min = daily_data.get('relative_humidity_2m_min', [])
        wind_speed_max = daily_data.get('wind_speed_10m_max', [])
        Tdew = []
        Vapr = []
        i  = 0
        while i < (len(tdew)):
            daily_mean = float(np.nanmean(tdew[i:i + 24]))  # Averaging every 24 hours
            Vapr.append(calculate_vapor_pressure_dew_point(daily_mean))
            Tdew.append(daily_mean)  # Averaging every 24 hours
            i = i + 24
        return {
            "Srad" : shortwave_radiation_sum,
            "Tmax" : temperature_max,
            "Tmin" : temperature_min,
            "Vapr" : Vapr,
            "Tdew" : Tdew,
            "RHmax": rh_max,
            "RHmin": rh_min,
            "Rain" : rain_sum,
            "ETref": et0_evapotranspiration,
            "MorP" : ["M"] * len(rain_sum),
            "Wndsp": convert_wind_speed(wind_speed_max)
        }
    else:
        print(f"Error: {response.status_code}")




def adjust_length(lst, length):
    return (lst * (length // len(lst) + 1))[:length]



# # Function to extract the date from a filename (assuming the date is part of the filename)
def extract_date_from_filename(filename):
    # Adjust this logic based on your file naming convention
    # Assuming date is in format 'YYYY-MM-DD' somewhere in the filename
    try:
        date_str = filename.split('_')[0]  # Adjust based on your filename structure
        return datetime.strptime(date_str, '%Y-%m-%d')
    except (IndexError, ValueError):
        return None

def fao_test():
        
    ndvi_folder = "/app/tools/aquacrop_test/sentinel_data/ndvi"
    files = [f for f in os.listdir(ndvi_folder) if os.path.isfile(os.path.join(ndvi_folder, f))]

    # Map filenames to dates
    file_date_map = {}

    for file in files:
        file_date = extract_date_from_filename(file)
        if file_date:
            file_date_map[file_date] = file

    # Prepare the date range and initialize data storage

    start_date = "2024-01-15"
    end_date = "2024-05-30"
    ft = "POLYGON((-7.678419088737144 31.66600208716224, -7.677561484332273 31.665936327983204, -7.677461044176198 31.664400837917725, -7.678434541068782 31.664367957767254, -7.678430677985574 31.66598564737157, -7.678419088737144 31.66600208716224))"
    # polygon = [loads(ft).__geo_interface__]  # Convert to GeoJSON-like dict
    polygon = loads(ft)


    start_date_ = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_ = datetime.strptime(end_date, '%Y-%m-%d')

    date_range = pd.date_range(start=start_date_, end=end_date_, freq='D')  # All days in the range
    fc_values = []
    h = []
    kcb_values = []

    # Loop over each day in the date range
    for current_date in date_range:
        if current_date in file_date_map:
            file_path = os.path.join(ndvi_folder, file_date_map[current_date])
            
            # Open and read the NDVI file
            # ndvi = gdal.Open(file_path)
            if os.path.exists(file_path):
                with rasterio.open(file_path) as src:

                    raster_crs = src.crs  # Get the raster's CRS

                    # print(src.)

                    transformer = Transformer.from_crs("EPSG:4326", raster_crs, always_xy=True)

                    transformed_coords = [
                        transformer.transform(x, y) for x, y in polygon.exterior.coords
                    ]

                    transformed_polygon_wkt = f"POLYGON(({', '.join([f'{x} {y}' for x, y in transformed_coords])}))"
                    transformed_polygon = loads(transformed_polygon_wkt)
                    polygon_geojson = [mapping(transformed_polygon)]

                    try:
                        out_image, out_transform = rasterio.mask.mask(src, polygon_geojson, crop=True)
                        # print("Clipping successful!")
                        # print("Clipped NDVI data:", out_image[0])

                        # Optionally, calculate the mean NDVI value within the polygon
                        mean_ndvi = out_image[0].mean()
                        # print("Mean NDVI within the polygon:", mean_ndvi)
                        if mean_ndvi != 0.0:
                            fc_values.append(float(1.33 * mean_ndvi - 0.20))
                            kcb_values.append(float(1.64 * (mean_ndvi - 0.14)))
                        else:
                            fc_values.append(np.nan)
                            kcb_values.append(np.nan)
            
                    except ValueError as e:
                        print(f"Error during clipping: {e}")
                    # out_image, out_transform = msk.mask(src, polygon, crop=True)

                    # out_meta = src.meta

                    # print("Clipped NDVI data:", out_image[0])

            
            else:
                print(f"Error: Could not open {file_path}")
                fc_values.append(np.nan)
                kcb_values.append(np.nan)
                continue
            
            # band1 = ndvi.GetRasterBand(1)
            # geo_transform = ndvi.GetGeoTransform()
            # projection = ndvi.GetProjection()

            # source_sr = osr.SpatialReference()
            # source_sr.ImportFromWkt(projection)

            # polygon = ogr.CreateGeometryFromWkt(ft)

            # target_sr = osr.SpatialReference()
            # target_sr.ImportFromEPSG(4326)  # WGS84
        
            # transform = osr.CoordinateTransformation(target_sr, source_sr)
            # polygon.Transform(transform)

            # min_x, max_x, min_y, max_y = polygon.GetEnvelope()

            # origin_x, pixel_width, _, origin_y, _, pixel_height = geo_transform
            # x_off = int((min_x - origin_x) / pixel_width)
            # y_off = int((max_y - origin_y) / pixel_height)
            # x_size = int((max_x - min_x) / pixel_width)
            # y_size = int((max_y - min_y) / pixel_height)


            # source_sr = osr.SpatialReference()
            # source_sr.ImportFromWkt(projection)
            # ndvi_data = band1.ReadAsArray(x_off, y_off, x_size, y_size)
            # Calculate fc and kcb 


            # Properly close the GDAL dataset
            # ndvi = None
            # break
        else:
            # If no file for the current date, append np.nan
            fc_values.append(np.nan)
            kcb_values.append(np.nan)
        h.append(np.nan)



def run_fao(fc_values, kcb_values, h, index, start_date, end_date):

    date_range = pd.date_range(start=start_date, end=end_date, freq='D')  # All days in the range

    index = date_range.strftime('%Y-%j')

    data = pd.DataFrame({
        'fc': fc_values,
        'Kcb': kcb_values,
        'h' : h,
    }, index=index)


    par = fao.Parameters()

    wth = fao.Weather(weather_data, index)

    airr = fao.AutoIrrigate()

    upd = fao.Update(data)

    mdl = fao.Model(date_range[0],date_range[-1], par, wth, autoirr=airr, upd=upd)

    mdl.run()

    print(mdl)

if __name__ == '__main__':
    weather_data = Open_meteo("2024-01-15", "2024-05-30", 31.66600208716224, -7.678419088737144)

    desired_length = len(weather_data["ETref"])
