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
from models_only.models import Farmer, Field, Irrigation_system, Irrigation_amount
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
from django.db.models import Prefetch
from rasterio.features import shapes


logger = logging.getLogger(__name__)

def get_session():

    copernicus_user = "hm.boukiili97@gmail.com"
    copernicus_password = "Mas123456789@"

    session = requests.Session()
    keycloak_token = get_keycloak(copernicus_user, copernicus_password)
    session.headers.update({"Authorization": f"Bearer {keycloak_token}"})

    return session

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

@shared_task
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

@shared_task         
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
    
            # with rasterio.open(output_path, "w", **meta) as dest:
            #     dest.write(out_image[0], 1)

            logger.info(f"Processed field {id} successfully. Output saved at {output_path}")

            return transformed_polygon.wkt, field_folder, meta

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

def get_irrigation():
    
    fields = Field.objects.prefetch_related(
    Prefetch('irrigation_systems', queryset=Irrigation_system.objects.prefetch_related(
        Prefetch('irrigation_amounts', queryset=Irrigation_amount.objects.all().order_by('date'))
    )))
    
    field_irrigation_amounts = {}

    # Iterate through each field
    for field in fields:
        amounts = []

        if field.irrigation_systems.exists():
            for system in field.irrigation_systems.all():
                for amount in system.irrigation_amounts.all():
                    amounts.append(amount.amount)

        if not amounts: amounts = None
        field_irrigation_amounts[field] = amounts
    return field_irrigation_amounts

@shared_task
def get_field_info(id, boundaries):

    field_folder = f"/app/Data/fao_output/{str(id)}/ndvi"
    files = [f for f in os.listdir(field_folder) if os.path.isfile(os.path.join(field_folder, f))]
    polygon = loads(boundaries)

    with rasterio.open(f'{field_folder}/{files[0]}') as src:
        raster_crs = src.crs
        transformer = Transformer.from_crs("EPSG:4326", raster_crs, always_xy=True)

        transformed_polygon = transform(transformer.transform, polygon)

    return transformed_polygon.wkt


@shared_task
def run_model():

    ndvi_folder = '/app/Data/ndvi'
    session = get_session()
    specific_tile = "T29SPR"  # Replace with your desired tile ID
    specific_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    response, specific_tile,  base_dir = check_data(specific_date, session, specific_tile)
    if response.status_code == 200:
        results = response.json()["value"]
        len_result = len(results)
        
        if len_result:

            # If the condition is met, process fields and then run fao_model
            if not os.path.exists(f'/app/Data/ndvi/{specific_date}_ndvi.tif'):
                folder = download_data(results, session, specific_date, specific_tile, base_dir)

                # Start calculating NDVI
                S2_ndvi(folder, ndvi_folder, specific_date)


            field_irrigation_amounts = get_irrigation()
    
            for field, amounts in field_irrigation_amounts.items():

                irrigation_amount = amounts if amounts else None
                polygon, field_folder, meta = process_field(field.boundaries.wkt, field.id, specific_date)
                task_chain = chain(
                    interpolate_ndvi.s(meta, field_folder),
                    fao_model.s()(polygon, field.boundaries[0][0], field.id, irrigation_amount)  # Explicitly set correct args
                )

                group_tasks = group(task_chain)
                group_tasks.apply_async()
        else:

            field_irrigation_amounts = get_irrigation()
            for field, amounts in field_irrigation_amounts.items():

                irrigation_amount = amounts if amounts else None

                task_chain = chain(
                    get_field_info.s(field.id, field.boundaries.wkt),
                    fao_model.s(field.boundaries[0][0], field.id, irrigation_amount)
                )

                group_tasks = group(task_chain)
                group_tasks.apply_async()
    else:
        logger.info(f"Error fetching data: {response.status_code} - {response.text}")
    return "Model completed successfully"

@shared_task
def process_new_field(field_id, boundaries_wkt, point, soumis_date):

    ndvi_folder = '/app/Data/ndvi'
    result_len = 0
    specific_tile = "T29SPR"  # Replace with your desired tile ID
    session = get_session()

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
                # file_name = f"{specific_date}_{specific_tile}.zip"    
                # save_path = os.path.join(base_dir, file_name)
                # if os.path.exists(save_path):
                #     folder = f"{base_dir}/{specific_date}_{specific_tile}"
                #     with zipfile.ZipFile(save_path, 'r') as zip_ref:
                #         zip_ref.extractall(folder)
                #         logger.info("Extraction complete!")
                #         # os.remove(save_path)
                #     print('data downloaded ...\n start ndvi process ...')
                S2_ndvi(folder, ndvi_folder, specific_date)
            print('processing data ....')
            # field_irrigation_amounts = get_irrigation()
            # for field, amounts in field_irrigation_amounts.items():
            polygon, field_folder, meta = process_field(boundaries_wkt, field_id, specific_date)
            # polygon, field_folder, meta = process_field(field.boundaries.wkt, field.id, specific_date)
                # interpolate_ndvi(meta, field_folder)
                # fao_model(polygon, [-7.680666, 31.66665], field.id , amounts)
                # print(field.id, amounts)
            # break
        logger.info(f'{specific_date}')
        specific_date = (datetime.strptime(specific_date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    session.close()
    # field_irrigation_amounts = get_irrigation()
    # for field, amounts in field_irrigation_amounts.items():
    #     folder = f"/app/Data/fao_output"
    #     field_folder = f"{folder}/{str(field.id)}/ndvi"
    interpolate_ndvi(meta, field_folder)
    print('running fao model ....')
    # fao_model(polygon, point, field_id , amounts)
    fao_model(polygon, point, field_id , None)


if __name__ == '__main__':
    process_new_field(32, 'POLYGON ((-7.680666 31.66665, -7.679964 31.666687, -7.679883 31.666271, -7.680436 31.666276, -7.680554 31.666536, -7.680666 31.66665))', [-7.680666, 31.66665], '2024-12-15')  # Valid input example
