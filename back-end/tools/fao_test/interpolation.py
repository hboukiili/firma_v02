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
from shapely.geometry import box


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


def extract_date_from_filename(filename):
    # Adjust this logic based on your file naming convention
    # Assuming date is in format 'YYYY-MM-DD' somewhere in the filename
    try:
        date_str = filename.split('_')[0]  # Adjust based on your filename structure
        return datetime.strptime(date_str, '%Y-%m-%d')
    except (IndexError, ValueError):
        return None

ndvi_folder = "/app/tools/aquacrop_test/sentinel_data/ndvi"
files = [f for f in os.listdir(ndvi_folder) if os.path.isfile(os.path.join(ndvi_folder, f))]

file_date_map = {}

for file in files:
    file_date = extract_date_from_filename(file)
    if file_date:
        file_date_map[file_date] = file

len_ndvi = None


start_date = "2024-01-15"
end_date = "2024-05-30"
ft = "POLYGON ((-7.678321344603916 31.66580238055144, -7.677650988631882 31.66569305230466, -7.6775747205875575 31.664825254781007, -7.678229020127901 31.6648901690497, -7.678333386926454 31.665795547539773, -7.678321344603916 31.66580238055144))"
polygon = loads(ft)


start_date_ = datetime.strptime(start_date, '%Y-%m-%d')
end_date_ = datetime.strptime(end_date, '%Y-%m-%d')

ndvi_data = []

date_range = pd.date_range(start=start_date_, end=end_date_, freq='D')  # All days in the range

for current_date in date_range:
    if current_date in file_date_map:
        file_path = os.path.join(ndvi_folder, file_date_map[current_date])
        with rasterio.open(file_path) as src:

            raster_crs = src.crs  # Get the raster's CRS

            # print(f"Raster CRS: {raster_crs}")

            # # Get the affine transform (used to calculate coordinates from pixel indices)
            # transform = src.transform
            # print(f"Affine Transform: {transform}")

            # # Get the bounding box of the raster (in the CRS of the raster)
            # bounds = src.bounds
            # print(f"Bounding Box: {bounds}")

            # # Print the coordinates of the corners of the raster (in the raster CRS)
            # print("Top-left corner:", (bounds.left, bounds.top))
            # print("Top-right corner:", (bounds.right, bounds.top))
            # print("Bottom-left corner:", (bounds.left, bounds.bottom))
            # print("Bottom-right corner:", (bounds.right, bounds.bottom))

            # exit()

            transformer = Transformer.from_crs("EPSG:4326", raster_crs, always_xy=True)

            transformed_coords = [
                transformer.transform(x, y) for x, y in polygon.exterior.coords
            ]


            transformed_polygon_wkt = f"POLYGON(({', '.join([f'{x} {y}' for x, y in transformed_coords])}))"

            transformed_polygon = loads(transformed_polygon_wkt)

            aligned_polygon = align_polygon_to_pixel(transformed_polygon, src.transform)

            polygon_geojson = [mapping(aligned_polygon)]

            exit()

#             try:
#                 out_image, out_transform = rasterio.mask.mask(src, polygon_geojson, crop=True)

#                 if len_ndvi == None:
#                     len_ndvi = out_image[0].shape
#                 if np.nanmean(out_image[0]) != 0.0:
#                     ndvi_data.append(out_image[0])
#                 else:
#                     ndvi_data.append(np.full((len_ndvi[0], len_ndvi[1]), np.nan))

#             except ValueError as e:
#                 print(f"Error during clipping: {e}")
    
#     else:
#         ndvi_data.append(np.full((len_ndvi[0], len_ndvi[1]), np.nan))

# i = 0
# while i < ndvi_data[0].shape[0]:  # Loop over rows
#     x = 0
#     while x < ndvi_data[0].shape[1]:  # Loop over columns
#         tst = []  # Reset tst for each pixel (i, x)
        
#         # Collect all NDVI values for the current pixel (i, x) across time
#         for ndvi in ndvi_data:
#             tst.append(ndvi[i][x])  # Append pixel value from each ndvi array
        
#         # Convert list to numpy array
#         to_np = np.array(tst)
        
#         # Find valid (non-NaN) indices
#         valid_indices = ~np.isnan(to_np)
#         valid_x = np.where(valid_indices)[0]  # Get the valid x indices
#         valid_y = to_np[valid_indices]  # Get the valid y values (non-NaN)

#         # Interpolate only if we have more than one valid data point
#         if len(valid_y) > 1:
#             f = interp1d(valid_x, valid_y, kind='linear', fill_value='extrapolate')
#             x_all = np.arange(len(ndvi_data))  # Full range of time steps
#             test_interpolated = f(x_all)
#         else:
#             # If only one valid point or no valid points, handle accordingly
#             test_interpolated = np.full(len(ndvi_data), np.nan) if len(valid_y) == 0 else np.full(len(ndvi_data), valid_y[0])
        
#         # Replace the original NDVI values with interpolated values
#         for z, ndvi in enumerate(ndvi_data):
#             ndvi[i][x] = test_interpolated[z]
        
#         x += 1  # Move to the next column (x)
    
#     i += 1  # Move to the next row (i)

# # Get metadata from one of the original files
# reference_file = os.path.join(ndvi_folder, file_date_map[list(file_date_map.keys())[0]])  # Use the first file for reference

# pixel_size_x = 10.0
# pixel_size_y = -10.0  
# min_x = min(x for x, y in transformed_coords)
# max_x = max(x for x, y in transformed_coords)
# min_y = min(y for x, y in transformed_coords)
# max_y = max(y for x, y in transformed_coords)


# # Open the reference file to get the metadata
# with rasterio.open(reference_file) as src:
#     meta = src.meta.copy()  # Copy the metadata
#     crs = src.crs  # Copy the CRS

# i = 0
# date_range = date_range.strftime('%Y-%m-%d')
# transform = Affine.translation(min_x, max_y) * Affine.scale(pixel_size_x, pixel_size_y)

# for date in date_range:

#     output_file = f"/app/tools/fao_test/interpolated_ndvi/{date}.tif"
    
#     meta.update({
#         "driver": "GTiff",
#         "height": ndvi_data[0].shape[0],
#         "width": ndvi_data[0].shape[1],
#         "count": 1,  # Single-band NDVI
#         "dtype": 'float32',  # Assuming NDVI is float
#         "crs": crs,  # Set the CRS
#         "transform": out_transform  # Set the affine transform
#     })

#     # Write the new interpolated NDVI data to a TIFF file
#     with rasterio.open(output_file, "w", **meta) as dest:
#         dest.write(ndvi_data[i], 1)  # Write the data to the first band

#     i += 1
# print("done")