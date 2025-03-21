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
# from scipy.interpolate import interp1d
from pyproj import Transformer
from shapely.geometry import mapping
from affine import Affine
import math
import matplotlib.pyplot as plt
from shapely.geometry import box


# def Open_meteo(start_date, end_date, lat, long):
#     # Set the URL for the Open-Meteo API (historical data)
#     url = "https://archive-api.open-meteo.com/v1/archive"

#     # Define parameters for the API request
#     params = {
#         "latitude": lat,  # Replace with the latitude of your location
#         "longitude": long,  # Replace with the longitude of your location
#         "start_date": start_date,  # Start date for historical data
#         "end_date": end_date,  # End date for historical data
#         "daily" : "rain_sum,shortwave_radiation_sum,et0_fao_evapotranspiration,temperature_2m_max,temperature_2m_min,relative_humidity_2m_max,relative_humidity_2m_min,wind_speed_10m_max",
#         # "hourly": "dewpoint_2m",
#         # 'current': 'temperature_2m, et0_fao_evapotranspiration',
#         "timezone": "Africa/Casablanca"  # Set your timezone
#     }


#     # Send the request to the Open-Meteo API
#     response = requests.get(url, params=params)

#     # Check if the request was successful
#     if response.status_code == 200:
#         data = response.json()
#         daily_data = data.get('daily', {})
#         et0_evapotranspiration = daily_data.get('et0_fao_evapotranspiration', [])
#         days = daily_data.get('time', [])
#         plt.plot(days, et0_evapotranspiration)
#         plt.xlabel('et0_evapotranspiration')
#         plt.ylabel('days')
#         plt.title('2018 et0')
#         plt.savefig('et0-2018.png') 
#         plt.show()
#         i = 0
#         while(i < len(days)):
#             print(days[i], et0_evapotranspiration[i])
#             i = i + 1
#     else:
#         print(f"Error: {response.status_code}")



ft = "POLYGON ((-7.678321344603916 31.66580238055144, -7.677650988631882 31.66569305230466, -7.6775747205875575 31.664825254781007, -7.678229020127901 31.6648901690497, -7.678333386926454 31.665795547539773, -7.678321344603916 31.66580238055144))"
ndvi_folder = "/app/tools/fao_test/fao_output/ndvi"
files = [f for f in os.listdir(ndvi_folder) if os.path.isfile(os.path.join(ndvi_folder, f))]

Kcb_folder = "/app/tools/fao_test/fao_output/kcb"
fc_folder  = "/app/tools/fao_test/fao_output/FC"

def extract_date(file_name):
    return datetime.strptime(file_name.split('.')[0], '%Y-%m-%d')

files = sorted(files, key=extract_date)

k = []
f = []
dates = []
n = []
for file in files:

    file_path = os.path.join(ndvi_folder, file)
    kcb_path = os.path.join(Kcb_folder, file)
    fc_path = os.path.join(fc_folder, file)
    dates.append(file.split('.')[0])
    with rasterio.open(file_path) as src, \
        rasterio.open(kcb_path) as src1, \
        rasterio.open(fc_path) as src2:

        ndvi = src.read(1)
        
        ndvi_mean = np.nanmean(ndvi)
        k_mean = 1.64 * (ndvi_mean - 0.14)
        f_mean = (1.33 * ndvi_mean) - 0.2
        
        if k_mean < 0:
            k_mean = 0
        
        if f_mean < 0:
            f_mean = 0

        k.append(k_mean)
        n.append(ndvi_mean)
        f.append(f_mean)
        print(dates[-1], ndvi_mean, f_mean, k_mean)

plt.plot(dates, k)
plt.xlabel('kcb')
plt.ylabel('days')
plt.title('kcb')
plt.savefig('kcb.png') 
plt.show()

plt.plot(dates, f)
plt.xlabel('fc')
plt.ylabel('days')
plt.title('fc orange, kcb bleu')
plt.savefig('fc.png') 
plt.show()

plt.plot(dates, n)
plt.xlabel('ndvi')
plt.ylabel('days')
plt.title('ndvi vert, kcb bleu, fc orange')
plt.savefig('ndvi.png') 
plt.show()
# flag = None

# polygon = loads(ft)

# def align_polygon_to_pixel(polygon, transform):
#     """
#     Aligns a polygon to the raster pixel grid based on its affine transform.
#     """
#     # Get the bounding box of the polygon
#     minx, miny, maxx, maxy = polygon.bounds
    
#     # Align to nearest pixel edges
#     aligned_minx = (np.floor((minx - transform.c) / transform.a) * transform.a) + transform.c
#     aligned_miny = (np.floor((miny - transform.f) / transform.e) * transform.e) + transform.f
#     aligned_maxx = (np.ceil((maxx - transform.c) / transform.a) * transform.a) + transform.c
#     aligned_maxy = (np.ceil((maxy - transform.f) / transform.e) * transform.e) + transform.f
    
#     # Create an aligned bounding box
#     aligned_polygon = box(aligned_minx, aligned_miny, aligned_maxx, aligned_maxy)
    
#     return aligned_polygon

# for file in files:

#     file_path = os.path.join(ndvi_folder, file)

#     with rasterio.open(file_path) as src:

#         raster_crs = src.crs  # Get the raster's CRS

#         if flag == None:

#             transformer = Transformer.from_crs("EPSG:4326", raster_crs, always_xy=True)

#             transformed_coords = [
#                 transformer.transform(x, y) for x, y in polygon.exterior.coords
#             ]


#             transformed_polygon_wkt = f"POLYGON(({', '.join([f'{x} {y}' for x, y in transformed_coords])}))"

#             transformed_polygon = loads(transformed_polygon_wkt)

#             aligned_polygon = align_polygon_to_pixel(transformed_polygon, src.transform)

#             polygon_geojson = [mapping(aligned_polygon)]

#         try:
#             out_image, out_transform = rasterio.mask.mask(src, polygon_geojson, crop=True)

#             print(file.split('.')[0].split('_')[0], np.nanmean(out_image))

#         except ValueError as e:
#             print(f"Error during clipping: {e}")

# if __name__ == '__main__':

#     weather_data = Open_meteo("2024-01-01", "2024-10-31", 31.66600208716224, -7.678419088737144)
