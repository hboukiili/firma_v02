import logging
from shapely.ops import transform
from rasterio.mask import mask
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
import zipfile
from shapely.wkt import loads
import pyfao56 as fao
from pyfao56.tools import forecast
import numpy as np
import os
from osgeo import gdal, ogr, osr
import pandas as pd
from scipy.interpolate import interp1d
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
from shapely.geometry import Polygon, mapping, shape
import numpy as np
import rasterio
import rasterio.mask
from rasterio.enums import Resampling
from shapely.geometry import Polygon, mapping
from rasterio.transform import from_bounds

def process_field(boundaries, id, date):

    folder = f"/app/Data/fao_output"
    polygon = loads(boundaries)
    # field_folder = f"{folder}/{str(id)}/ndvi"
    field_folder = './'
    # try:
    with rasterio.open(f'/app/Data/ndvi/{date}_ndvi.tif') as src:

        raster_crs = src.crs
        meta = src.meta.copy()
        transformer = Transformer.from_crs("EPSG:4326", raster_crs, always_xy=True)

        # # Transform polygon
        transformed_polygon = transform(transformer.transform, polygon)
        # print(transformed_polygon)
        if not transformed_polygon.is_valid:
            transformed_polygon = transformed_polygon.buffer(0)

        # Align polygon to pixel grid
        aligned_polygon = align_polygon_to_pixel_outside(transformed_polygon, src.transform, 10)
        polygon_geojson = [mapping(aligned_polygon)]
        print(polygon_geojson, transformed_polygon)
        # # Clip raster
        out_image, out_transform = mask(src, polygon_geojson, crop=True, nodata=-9999)
        meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform,
            "nodata": -9999,
        })

        output_path = os.path.join(field_folder, f"{date}.tif")

        if not os.path.exists(field_folder):
            os.makedirs(field_folder)
            os.chmod(field_folder, 0o777)

        with rasterio.open(output_path, "w", **meta) as dest:
            dest.write(out_image[0], 1)
        print(output_path)

import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling, calculate_default_transform
from rasterio.mask import mask
from rasterio.transform import from_origin
from shapely.geometry import Polygon, mapping
from shapely.wkt import loads

import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling, calculate_default_transform
from rasterio.mask import mask
from rasterio.transform import from_origin
from shapely.geometry import Polygon, mapping
from shapely.wkt import loads

def align_polygon_to_pixel_outside(polygon, transform, pixel_size):
    """
    Aligns a polygon to the nearest raster pixel grid, ensuring the entire polygon
    is contained within the new aligned shape while minimizing extra no-data pixels.

    Parameters:
    - polygon (Shapely Polygon): The input polygon.
    - transform (Affine): The raster transform.
    - pixel_size (float): The pixel resolution (e.g., 10m or 1m).

    Returns:
    - aligned_polygon (Shapely Polygon): The polygon aligned to the nearest pixel grid outside.
    """
    minx, miny, maxx, maxy = polygon.bounds

    # Align to the nearest **outside** pixel edges
    aligned_minx = (np.floor((minx - transform.c) / pixel_size) * pixel_size) + transform.c
    aligned_miny = (np.floor((miny - transform.f) / pixel_size) * pixel_size) + transform.f
    aligned_maxx = (np.ceil((maxx - transform.c) / pixel_size) * pixel_size) + transform.c
    aligned_maxy = (np.ceil((maxy - transform.f) / pixel_size) * pixel_size) + transform.f

    # Create an aligned polygon
    aligned_polygon = Polygon([
        (aligned_minx, aligned_miny),
        (aligned_maxx, aligned_miny),
        (aligned_maxx, aligned_maxy),
        (aligned_minx, aligned_maxy),
        (aligned_minx, aligned_miny)  # Close the polygon
    ])

    return aligned_polygon

def process_raster_for_visualization(input_raster, polygon, output_raster):
    """
    Reads a single-band 10m raster, aligns the polygon to the nearest pixel grid,
    clips it, resamples to 1m per pixel, and then clips the actual polygon for visualization.

    Parameters:
    - input_raster (str): Path to the input 10m raster file.
    - polygon (Shapely Polygon): The polygon to clip from the raster.
    - output_raster (str): Path to save the final processed raster.
    """
    polygon = loads(polygon)
    with rasterio.open(input_raster) as src:
        pixel_size = src.transform.a  # Assuming square pixels (10m initially)

        # Align polygon to the nearest **outside** pixel grid
        aligned_polygon = align_polygon_to_pixel_outside(polygon, src.transform, pixel_size)

        # Convert to GeoJSON format for clipping
        aligned_geojson = [mapping(aligned_polygon)]

        # Clip raster using the aligned polygon
        clipped_raster, clipped_transform = mask(src, aligned_geojson, crop=True, nodata=-9999)

        # Calculate the new transform and dimensions for 1m resolution
        new_transform, new_width, new_height = calculate_default_transform(
            src.crs, src.crs, clipped_raster.shape[2] * 10, clipped_raster.shape[1] * 10,
            *aligned_polygon.bounds, resolution=(1, 1)
        )
        print(src.crs, src.crs, clipped_raster.shape[2] * 10, clipped_raster.shape[1] * 10)
        print(*aligned_polygon.bounds)
        print(new_transform, new_height, new_width)
        # Create an empty array for the resampled raster
        resampled_raster = np.empty((new_height, new_width), dtype=src.dtypes[0])

        # Perform resampling
        reproject(
            source=clipped_raster[0],  # Single-band
            destination=resampled_raster,
            src_transform=clipped_transform,
            src_crs=src.crs,
            dst_transform=new_transform,
            dst_crs=src.crs,
            resampling=Resampling.bilinear
        )

        # Save resampled raster
        new_meta = src.meta.copy()
        new_meta.update({
            "driver": "GTiff",
            "height": new_height,
            "width": new_width,
            "transform": new_transform,
        })

        with rasterio.open(output_raster, 'w', **new_meta) as dst:
            dst.write(resampled_raster, 1)  # Single-band write

        # Clip the **exact** polygon from the resampled raster
        actual_geojson = [mapping(polygon)]
        with rasterio.open(output_raster) as final_raster:
            final_clipped, final_transform = mask(final_raster, actual_geojson, crop=True, nodata=np.nan)

        # Save final clipped raster
        final_meta = final_raster.meta.copy()
        final_meta.update({
            "transform": final_transform,
            "height": final_clipped.shape[1],
            "width": final_clipped.shape[2],
            "nodata": np.nan,
        })

        with rasterio.open(output_raster, 'w', **final_meta) as dst:
            dst.write(final_clipped[0], 1)  # Single-band write

    return output_raster

# process_field('POLYGON ((-7.680666 31.66665, -7.679964 31.666687, -7.679883 31.666271, -7.680436 31.666276, -7.680554 31.666536, -7.680666 31.66665))', 32, '2025-01-25')
process_raster_for_visualization('/app/Data/fao_output/32/ndvi/2024-12-16.tif', 'POLYGON ((625071.9003894652 3504243.3785424978, 625138.4051854884 3504248.2848903243, 625146.6424093188 3504202.2642143983, 625094.2073021412 3504202.184334228, 625082.6715574508 3504230.8700385797, 625071.9003894652 3504243.3785424978))', '/app/Data/2025-01-25.tif')