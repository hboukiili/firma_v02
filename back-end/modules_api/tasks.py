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
import zipfile
from .tools.ndvi_calcul import S2_ndvi

logger = logging.getLogger(__name__)


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
def run_model():

    ndvi_folder = '/app/Data/ndvi'
    copernicus_user = "hm.boukiili97@gmail.com"
    copernicus_password = "Mas123456789@"

    specific_tile = "T29SPR"  # Replace with your desired tile ID
    # specific_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    specific_date = '2024-12-06'
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

    if response.status_code == 200:
        results = response.json()["value"]
        if len(results):
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
    
            #start calculatigng ndvi
            S2_ndvi(folder, ndvi_folder)

        else :
            logger.info('no data has been found')
    else:
        logger.info(f"Error fetching data: {response.status_code} - {response.text}")
        return "Model completed successfully"
