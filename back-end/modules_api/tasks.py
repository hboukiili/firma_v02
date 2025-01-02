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
from shapely.geometry import mapping
from affine import Affine
import math
from shapely.geometry import box
from celery import group
from .tools.fao_raster import fao_model
from .tools.geoserver_tools import *
from celery import chain


logger = logging.getLogger(__name__)



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


def interpolate_ndvi(ndvi_data, meta, date_range, field_folder):
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
    
    # Write the interpolated NDVI rasters to files
    for i, date in enumerate(date_range):
        output_file = f"{field_folder}/{date.strftime('%Y-%m-%d')}.tif"
        with rasterio.open(output_file, "w", **meta) as dest:
            dest.write(interpolated_ndvi[i], 1)  # Write the data to the first band
            dest.update_tags(TIFFTAG_DATETIME=date.strftime('%Y%m%d'),Time=date.strftime('%Y%m%d'))
            logging.info(f"{date.strftime('%Y-%m-%d')} Done")

            
@shared_task
def process_field(boundaries, id, date):

    folder = f"/app/Data/fao_output"
    polygon = loads(boundaries)
    field_folder = f"{folder}/{str(id)}/ndvi"

    try:
        with rasterio.open(f'/app/Data/ndvi/{date}_ndvi.tif') as src:
    
            raster_crs = src.crs
            meta = src.meta.copy()
            transformer = Transformer.from_crs("EPSG:4326", raster_crs, always_xy=True)

            # # Transform polygon
            transformed_polygon = transform(transformer.transform, polygon)
            print(transformed_polygon)
            if not transformed_polygon.is_valid:
                transformed_polygon = transformed_polygon.buffer(0)

            # Align polygon to pixel grid
            aligned_polygon = align_polygon_to_pixel(transformed_polygon, src.transform)
            polygon_geojson = [mapping(aligned_polygon)]
            print(polygon_geojson, transformed_polygon)
            # # Clip raster
            out_image, out_transform = mask(src, polygon_geojson, crop=True)
            print(out_transform, out_image.shape)
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

            files = [f for f in os.listdir(field_folder) if os.path.isfile(os.path.join(field_folder, f))]
            
            if len(files) > 1:

                files = sorted(files, key=lambda x: x.split('.')[0])


                date_range = pd.date_range(start=files[0].split('.')[0], end=files[-1].split('.')[0], freq='D')  # All days in the range

                ndvi_data = []

                for day in date_range:
                
                    day = day.strftime('%Y-%m-%d')
                    tif_path = f"{field_folder}/{day}.tif"

                    if os.path.exists(tif_path):
                        with rasterio.open(tif_path) as tif:
                            ndvi = tif.read(1)
                            ndvi_data.append(ndvi)
                    else :
                        ndvi_data.append(np.full((ndvi.shape[0], ndvi.shape[1]), np.nan))

                interpolate_ndvi(ndvi_data, meta, date_range, field_folder)



    except rasterio.errors.RasterioIOError as e:
        logger.error(f"RasterIO Error for field {id}: {e}")
    except Exception as e:
        logger.error(f"Unexpected Error for field {id}: {e}")
 

def check_data(specific_date):

    try:

        copernicus_user = "hm.boukiili97@gmail.com"
        copernicus_password = "Mas123456789@"

        specific_tile = "T29SPR"  # Replace with your desired tile ID
        base_dir = "/app/Data"

        session = requests.Session()
        keycloak_token = get_keycloak(copernicus_user, copernicus_password)
        session.headers.update({"Authorization": f"Bearer {keycloak_token}"})

        query_url = (
            f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?"
            f"$filter=contains(Name, '{specific_tile}') "
            f"and ContentDate/Start ge {specific_date}T00:00:00.000Z "
            f"and ContentDate/Start le {specific_date}T23:59:59.999Z "
            f"and contains(Name, 'L2A')"
        )

        response = session.get(query_url)
        return response, specific_tile, session, base_dir

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
            os.remove(save_path)
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
                    fao_model.s(field.boundaries[0][0], field.id)
                ) for field in All_fields
            )

            group_tasks.apply_async()

        else:

            All_fields = Field.objects.all()

            model_tasks = group(fao_model.s('', field.boundaries[0][0], field.id) for field in All_fields)
            model_tasks.apply_async()


    else:
        logger.info(f"Error fetching data: {response.status_code} - {response.text}")
    return "Model completed successfully"

@shared_task
def run_geoserver(r, field_id):

    path = f'/app/Data/fao_output/{str(field_id)}'
    create_workspace(str(field_id))

    fodlers = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

    for folder in fodlers:
        create_store(field_id, folder, f"/data/{str(field_id)}/{folder}")
        create_indexer_and_timeregex(f"{path}/{folder}")
        publish_layer(str(field_id), folder, folder)
        enable_time_dimension(str(field_id), folder)

@shared_task
def process_new_field(field_id, boundaries_wkt, point):

    ndvi_folder = '/app/Data/ndvi'
    result_len = 0
    max_retries = 10
    retry_count = 0
    specific_date = (datetime.now()).strftime('%Y-%m-%d')

    while result_len == 0 and retry_count < max_retries:

        response, specific_tile, session, base_dir = check_data(specific_date)
        if response.status_code != 200:
            logger.error(f"Failed to fetch data: {response.status_code}")
            session.close()
            break

        results = response.json()["value"]
        result_len = len(results)
        if result_len:

            folder = download_data(results, session, specific_date, specific_tile, base_dir)
            
            S2_ndvi(folder, ndvi_folder, specific_date)
            
            create_workspace(field_id)

            chain(
                process_field.s(boundaries_wkt, field_id, specific_date),
                fao_model.s(point, field_id),
                run_geoserver.s(field_id)
            )()
            break
        else:

            logger.info(f'no data has been found for {specific_date}')
            specific_date = (datetime.strptime(specific_date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
            retry_count += 1
    session.close()


if __name__ == '__main__':
    process_new_field(119, '', '')