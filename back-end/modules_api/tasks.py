from celery import shared_task
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
from .tools.ndvi_calcul import S2_ndvi
from models_only.models import Farmer, Field
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
from shapely.geometry import mapping, Polygon
from affine import Affine
import math
from shapely.geometry import box
from celery import group
from .tools.fao_raster import fao_model
from .tools.geoserver_tools import *
from celery import chain


logger = logging.getLogger(__name__)



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

def get_keycloak(username: str, password: str) -> str:
    data = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password",
    }
    try:
        r = requests.post(
            "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
            data=data,
        )
        r.raise_for_status()
    except Exception as e:
        raise Exception(
            f"Keycloak token creation failed. Reponse from the server was: {r.json()}"
        )
    return r.json()["access_token"]

def interpolate_ndvi(meta, field_folder):
    """
    Interpolates NDVI data for all pixels across time using vectorized operations.

    Parameters:
    - ndvi_data: List of 2D NDVI arrays (time_steps, height, width)
    - meta: Metadata dictionary for writing output rasters (must include 'driver', 'dtype', 'crs', 'transform', etc.)
    - date_range: List of datetime objects corresponding to each time step
    - field_folder: Folder path for saving output rasters

    Returns:
    - None (writes interpolated NDVI rasters to files)
    """
    
    files = [f for f in os.listdir(field_folder) if os.path.isfile(os.path.join(field_folder, f))]
    
    if len(files) <= 1: return

    files = sorted(files, key=lambda x: x.split('.')[0])

    date_range = pd.date_range(start=files[0].split('.')[0], end=files[-1].split('.')[0], freq='D')  # All days in the range

    ndvi_data = []

    for day in date_range:
    
        day = day.strftime('%Y-%m-%d')
        tif_path = f"{field_folder}/{day}.tif"

        if os.path.exists(tif_path):
            with rasterio.open(tif_path) as tif:
                ndvi = tif.read(1)
                if np.nanmean(ndvi) != 0.0:
                    ndvi_data.append(ndvi)
                else:
                    ndvi_data.append(np.full((ndvi.shape[0], ndvi.shape[1]), np.nan))
        else :
            ndvi_data.append(np.full((ndvi.shape[0], ndvi.shape[1]), np.nan))

    # Combine NDVI rasters into a 3D stack
    ndvi_stack = np.array(ndvi_data)  # Shape: (time_steps, height, width)
    
    # Time indices for interpolation
    time_indices = np.arange(ndvi_stack.shape[0])  # [0, 1, ..., time_steps-1]
    
    # Initialize an empty array to store interpolated values
    interpolated_ndvi = np.empty_like(ndvi_stack)
    
    # Interpolate each pixel's time series
    for i in range(ndvi_stack.shape[1]):  # Loop over height (rows)
        for j in range(ndvi_stack.shape[2]):  # Loop over width (columns)
            pixel_values = ndvi_stack[:, i, j]  # Extract time series for the pixel
            valid_times = time_indices[~np.isnan(pixel_values)]
            valid_values = pixel_values[~np.isnan(pixel_values)]
            
            if len(valid_values) > 1:  # Interpolate only if there are multiple valid points
                interp_func = interp1d(valid_times, valid_values, bounds_error=False, fill_value="extrapolate")
                interpolated_ndvi[:, i, j] = interp_func(time_indices)
            elif len(valid_values) == 1:  # Single valid point
                interpolated_ndvi[:, i, j] = np.full(len(time_indices), valid_values[0])
            else:  # No valid points
                interpolated_ndvi[:, i, j] = np.full(len(time_indices), np.nan)
    
    # Write the interpolated NDVI rasters to files
    for i, date in enumerate(date_range):
        output_file = f"{field_folder}/{date.strftime('%Y-%m-%d')}.tif"
        with rasterio.open(output_file, "w", **meta) as dest:
            dest.write(interpolated_ndvi[i], 1)  # Write the data to the first band
            # dest.update_tags(TIFFTAG_DATETIME=date.strftime('%Y%m%d'), Time=date.strftime('%Y%m%d'))
            logging.info(f"{date.strftime('%Y-%m-%d')} Done")
            
def process_field(boundaries, id, date):

    folder = f"/app/Data/fao_output"
    polygon = loads(boundaries)
    field_folder = f"{folder}/{str(id)}/ndvi"
    # field_folder = f"/app/Data/test"
    try:
        with rasterio.open(f'/app/Data/ndvi/{date}_ndvi.tif') as src:
    
            raster_crs = src.crs
            meta = src.meta.copy()
            pixel_size = src.transform.a  # Assuming square pixels (10m initially)
            transformer = Transformer.from_crs("EPSG:4326", raster_crs, always_xy=True)

            # # Transform polygon
            transformed_polygon = transform(transformer.transform, polygon)
            if not transformed_polygon.is_valid:
                transformed_polygon = transformed_polygon.buffer(0)

            # Align polygon to pixel grid
            aligned_polygon = align_polygon_to_pixel_outside(transformed_polygon, src.transform, pixel_size)
            polygon_geojson = [mapping(aligned_polygon)]
            # # Clip raster
            out_image, out_transform = mask(src, polygon_geojson, crop=True)

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

            logger.info(f"Processed field {id} successfully. Output saved at {output_path}")

            return transformed_polygon, meta, field_folder

    except rasterio.errors.RasterioIOError as e:
        logger.error(f"RasterIO Error for field {id}: {e}")
    except Exception as e:
        logger.error(f"Unexpected Error for field {id}: {e}")


def check_data(specific_date, session, specific_tile):

    try:

        base_dir = "/app/Data"

        query_url = (
            f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?"
            f"$filter=contains(Name, '{specific_tile}') "
            f"and ContentDate/Start ge {specific_date}T00:00:00.000Z "
            f"and ContentDate/Start le {specific_date}T23:59:59.999Z "
            f"and contains(Name, 'L2A')"
        )

        response = session.get(query_url)
        return response, specific_tile, base_dir

    except requests.exceptions.RequestException as e:
        logger.error(f"Error in check_data: {e}")
        return None, None, None, None, None


def download_data(results, session, specific_date, specific_tile, base_dir):

    try:

        product_id = results[0]["Id"]
        url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products({product_id})/$value"
        response = session.get(url, allow_redirects=False)
        logger.info('got Response ...')
        while response.status_code in (301, 302, 303, 307):
            logger.info('redirected ...')
            url = response.headers["Location"]
            logger.info(url)
            response = session.get(url, allow_redirects=False)
        logger.info('start downlaoding ...')

        file_name = f"{specific_date}_{specific_tile}.zip"
        save_path = os.path.join(base_dir, file_name)
        with open(save_path, "wb") as file:
            logger.info(f"Downloading {file_name}...")
            file.write(response.content)
            logger.info(f"Saved to {save_path}.")
        folder = f"{base_dir}/{specific_date}_{specific_tile}"
        with zipfile.ZipFile(save_path, 'r') as zip_ref:
            zip_ref.extractall(folder)
            logger.info("Extraction complete!")
            # os.remove(save_path)
        return folder
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading data: {e}")
        return None  # Indicate failure

@shared_task
def run_model():

    ndvi_folder = '/app/Data/ndvi'
    specific_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    response, specific_tile, session, base_dir = check_data(specific_date)
    if response.status_code == 200:
        results = response.json()["value"]
        len_result = len(results)
        if len_result:

            # If the condition is met, process fields and then run fao_model
            folder = download_data(results, session, specific_date, specific_tile, base_dir)

            # Start calculating NDVI
            S2_ndvi(folder, ndvi_folder, specific_date)

            All_fields = Field.objects.all()

            # Create a group of chains for `process_field` and `fao_model`
            group_tasks = group(
                chain(
                    process_field.s(field.boundaries.wkt, field.id, specific_date),
                    fao_model.s(field.boundaries[0][0], field.id, False)
                ) for field in All_fields
            )

            group_tasks.apply_async()

        else:

            All_fields = Field.objects.all()

            model_tasks = group(fao_model.s(field.boundaries[0][0], field.id) for field in All_fields)
            model_tasks.apply_async()


    else:
        logger.info(f"Error fetching data: {response.status_code} - {response.text}")
    return "Model completed successfully"

@shared_task
def process_new_field(field_id, boundaries_wkt, point, soumis_date):

    ndvi_folder = '/app/Data/ndvi'
    result_len = 0
    copernicus_user = "hm.boukiili97@gmail.com"
    copernicus_password = "Mas123456789@"

    specific_tile = "T29SPR"  # Replace with your desired tile ID
    session = requests.Session()
    keycloak_token = get_keycloak(copernicus_user, copernicus_password)
    session.headers.update({"Authorization": f"Bearer {keycloak_token}"})

    specific_date = (datetime.now()).strftime('%Y-%m-%d')

    while soumis_date != specific_date:
        response, specific_tile,  base_dir = check_data(specific_date, session, specific_tile)
        if response.status_code != 200:
            logger.error(f"Failed to fetch data: {response.status_code}")
            session.close()
            break

        results = response.json()["value"]
        result_len = len(results)
        print(specific_date, result_len)
        if result_len:

            if not os.path.exists(f'/app/Data/ndvi/{specific_date}_ndvi.tif'):
                print('starting downloading data')
                folder = download_data(results, session, specific_date, specific_tile, base_dir)
                print('data downloaded ...\n start ndvi process ...')
                S2_ndvi(folder, ndvi_folder, specific_date)

            print('processing data ....')
            polygon, meta, field_folder = process_field(boundaries_wkt, field_id, specific_date)
        logger.info(f'{specific_date}')
        specific_date = (datetime.strptime(specific_date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    session.close()

    interpolate_ndvi(meta, field_folder)
    print('running fao model ....')
    irr = [0,00,0,0,0,0,0,0,0,0,0,14.12396349,0,0,0,0,0,0,14.12396349,0,0,0,0,0,0,0,0,0,0,0,9.415975658,0,0,0,0,0,0,0]
    fao_model(point, field_id, polygon, irr)


if __name__ == '__main__':
    process_new_field(47, 'POLYGON ((-7.679181 31.666372, -7.679148 31.666125, -7.678735 31.666057, -7.678456 31.666039, -7.678542 31.666386, -7.679181 31.666372))', [-7.680666, 31.66665], '2024-12-16')  # Valid input example
