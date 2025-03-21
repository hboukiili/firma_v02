from shapely.ops import transform
from rasterio.mask import mask
from celery import shared_task
import logging
from celery.result import AsyncResult
import requests
from datetime import date, timedelta, datetime
import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape
import os
import rasterio
from rasterio.enums import Resampling
# import zipfile
# from .tools.ndvi_calcul import S2_ndvi
# from models_only.models import Farmer, Field
from shapely.wkt import loads
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
from scipy.interpolate import interp1d
from pyproj import Transformer
from shapely.geometry import mapping
from affine import Affine
import math
from shapely.geometry import box
from celery import group

pd.set_option('display.max_rows', None)  # This will display all rows
pd.set_option('display.max_columns', None)  # This will display all columns


from shapely.geometry import box
from shapely.ops import transform
from shapely.geometry import mapping
from rasterio.mask import mask
import numpy as np
import rasterio
from pyproj import Transformer

def align_polygon_to_pixel(polygon, transform):
    """
    Aligns a polygon to the raster pixel grid based on its affine transform.
    """
    # Get the bounding box of the polygon
    minx, miny, maxx, maxy = polygon.bounds

    # Align to nearest pixel edges
    aligned_minx = (np.floor((minx - transform.c) / transform.a) * transform.a) + transform.c
    aligned_miny = (np.floor((miny - transform.f) / transform.e) * transform.e) + transform.f
    aligned_maxx = (np.ceil((maxx - transform.c) / transform.a) * transform.a) + transform.c
    aligned_maxy = (np.ceil((maxy - transform.f) / transform.e) * transform.e) + transform.f

    # Create an aligned bounding box
    aligned_polygon = box(aligned_minx, aligned_miny, aligned_maxx, aligned_maxy)

    return aligned_polygon


field_folder = "/app/Data/fao_output/118/ndvi"

def interpolate_ndvi(ndvi_data):
    """
    Interpolates NDVI data for all pixels across time using vectorized operations.
    """
    # Combine NDVI rasters into a 3D stack
    ndvi_stack = np.array(ndvi_data)  # Shape: (time_steps, height, width)
    
    # Create a mask for valid (non-NaN) data
    valid_mask = ~np.isnan(ndvi_stack)  # Shape: (time_steps, height, width)
    
    # Time indices for interpolation
    time_indices = np.arange(ndvi_stack.shape[0])  # [0, 1, ..., time_steps-1]
    
    # Vectorized interpolation along the time axis
    def interpolate_pixel(pixel_values):
        valid_times = time_indices[~np.isnan(pixel_values)]
        valid_values = pixel_values[~np.isnan(pixel_values)]
        if len(valid_values) > 1:  # Interpolate only if there are multiple valid points
            interp_func = interp1d(valid_times, valid_values, bounds_error=False, fill_value="extrapolate")
            return interp_func(time_indices)
        elif len(valid_values) == 1:
            return np.full(len(time_indices), valid_values[0])  # Single valid point
        else:
            return np.full(len(time_indices), np.nan)  # No valid points

    interpolated_ndvi = np.apply_along_axis(interpolate_pixel, axis=0, arr=ndvi_stack)  # Shape: (time_steps, height, width)

    for i, date in enumerate(date_range):
        output_file = f"{field_folder}/{date.strftime('%Y-%m-%d')}.tif"
        with rasterio.open(output_file, "w", **meta) as dest:
            dest.write(interpolated_ndvi[i], 1)  # Write the data to the first band
            logging.info(f"{date.strftime('%Y-%m-%d')} Done")


# Load raster and align polygon
ndvi_data = []
ndvi_folder = "/app/Data/ndvi"
files = [f for f in os.listdir(ndvi_folder) if os.path.isfile(os.path.join(ndvi_folder, f))]
files = sorted(files, key=lambda x: x.split('.')[0])

polygon = loads("POLYGON ((-7.897958 31.624195, -7.897026 31.624232, -7.897133 31.622011, -7.89798 31.622011, -7.897958 31.624195))")
date_range = pd.date_range(start=files[0].split('.')[0].split('_')[0], end=files[-1].split('.')[0].split('_')[0], freq='D')  # All days in the range

# for test in date_range:
#     day = test.strftime('%Y-%m-%d')
#     path = f"{ndvi_folder}/{day}_ndvi.tif"
#     if os.path.exists(path):

#         with rasterio.open(path) as src:
#             raster_crs = src.crs
#             meta = src.meta.copy()

#             transformer = Transformer.from_crs("EPSG:4326", raster_crs, always_xy=True)
#             transformed_polygon = transform(transformer.transform, polygon)
   
#             if not transformed_polygon.is_valid:
#                 transformed_polygon = transformed_polygon.buffer(0)
   
#             aligned_polygon = align_polygon_to_pixel(transformed_polygon, src.transform)
   
#             polygon_geojson = [mapping(aligned_polygon)]
   
#             try:
#                 out_image, out_transform = mask(src, polygon_geojson, crop=True)
#                 ndvi_data.append(out_image[0])
#                 # # Save output raster
#                 meta.update({
#                     "driver": "GTiff",
#                     "height": out_image[0].shape[0],
#                     "width": out_image[0].shape[1],
#                     "transform": out_transform,
#                 })

#                 output_path = f"/app/Data/fao_output/118/ndvi/{day}.tif"
#                 with rasterio.open(output_path, "w", **meta) as dest:
#                     dest.write(out_image[0], 1)  # Write the first band directly
#                 print(f"Saved aligned raster to {output_path}")
#             except Exception as e:
#                 print(f"Error during raster masking: {e}")
#     else :
#         ndvi_data.append(np.full((out_image[0].shape[0], out_image[0].shape[1]), np.nan))

# print(len(ndvi_data))

# interpolate_ndvi(ndvi_data)

ndvi_folder = "/app/Data/fao_output/118/ndvi"
files = [f for f in os.listdir(ndvi_folder) if os.path.isfile(os.path.join(ndvi_folder, f))]
files = sorted(files, key=lambda x: x.split('.')[0])

for file in files:
    path = f"{ndvi_folder}/{file}"
    with rasterio.open(path) as src:
        out_image = src.read(1)
        # print(src.profile)
    print(file,' mean ', np.nanmean(out_image), 'min ' ,np.nanmin(out_image), 'max ', np.nanmax(out_image))
# for out_image in ndvi_data:
    # print(out_image.shape)