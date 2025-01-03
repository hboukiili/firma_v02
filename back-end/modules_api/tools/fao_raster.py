from celery import shared_task
import logging
import numpy as np
import os
import rasterio
from rasterio.transform import Affine
from datetime import datetime
import pandas as pd
from pyfao56 import Parameters, Weather, AutoIrrigate, Model, Update
from pyproj import Transformer
from shapely.geometry import mapping
from shapely.ops import transform
from rasterio.mask import mask
from .Open_meteo import fao_Open_meteo, forcast_fao_Open_meteo
from .geoserver_tools import publish_single_layer, create_workspace

pd.set_option('display.max_rows', None)  # This will display all rows
pd.set_option('display.max_columns', None)  # This will display all columns


# Initialize logger
logger = logging.getLogger(__name__)


def load_raster_files(folder):
    """Load all NDVI rasters from a folder and return as a list of arrays."""
    files = sorted([f for f in os.listdir(folder) if f.endswith(".tif")], key=lambda x: x.split('.')[0])
    rasters = []
    meta = None

    for file in files:
        with rasterio.open(os.path.join(folder, file)) as src:
            if meta is None:
                meta = src.meta.copy()
            rasters.append(src.read(1))  # Read the first band

    return rasters, meta

def calculate_fc_kcb(ndvis):
    """Calculate FC and Kcb arrays for NDVI rasters."""
    ndvis = np.stack(ndvis)  # Stack into a 3D array (time, height, width)
    fc = 1.33 * ndvis - 0.20
    kcb = 1.64 * (ndvis - 0.14)

    # Ensure values are non-negative
    fc[fc < 0] = 0
    kcb[kcb < 0] = 0

    return fc, kcb

def run_fao_model(fc, kcb, h, weather_data, index, par, airr):
    """Run the FAO model for a single pixel."""
    data = pd.DataFrame({'fc': fc, 'Kcb': kcb, 'h': h}, index=index)
    update = Update(data)
    model = Model(index[0], index[-1], par, weather_data, autoirr=airr, upd=update)
    model.run()
    return model.odata

def save_raster(data_dict, output_folder, meta, shape):
    """Save computed rasters to disk."""
    for date_str, data in data_dict.items():
        parsed_date = datetime.strptime(date_str, '%Y-%j')
        date = parsed_date.strftime('%Y-%m-%d')
        timestamp = parsed_date.strftime('%Y-%m-%d')  # ISO8601 format
        output_path = os.path.join(output_folder, f"{output_folder.split('/')[-1]}_{date}.tif")
        os.makedirs(output_folder, mode=0o777, exist_ok=True)
        os.chmod(output_folder, 0o777)

        with rasterio.open(output_path, "w", **{**meta, "height": shape[0], "width": shape[1]}) as dest:
            dest.write(data, 1)
            dest.update_tags(TIFFTAG_DATETIME=timestamp,Time=timestamp)
            os.chmod(output_path, 0o777)
        
        publish_single_layer(output_folder.split('/')[-2], 
                                output_path.split('/')[-1], 
                                output_folder.split('/')[-1])
    
@shared_task
def process_field(ndvi_folder, output_folder, weather_data, index, par, airr):
    """Process NDVI rasters and run the FAO model."""
    logger.info("Starting field processing...")

    # Load NDVI rasters
    ndvis, meta = load_raster_files(ndvi_folder)
    
    len_ndvis, len_index = len(ndvis), len(index)

    while len_ndvis < len_index:
        ndvis.append(ndvis[-1])
        len_ndvis += 1
    
    h = [np.nan] * len(ndvis)

    # Calculate FC and Kcb arrays
    fc, kcb = calculate_fc_kcb(ndvis)

    # Initialize dictionaries for outputs
    results = {param: {} for param in ['FC', 'Kcb', 'E', 'Zr', 'Ks', 'Kcadj', 'ETcadj', 'T', 'DP', 'Irrig', 'Rain', 'Runoff', 'ETref']}
    
    for i in range(fc.shape[1]):  # Loop over rows
        for x in range(fc.shape[2]):  # Loop over columns
            # try:
                # Extract pixel values over time
                fc_pixel = fc[:, i, x]
                kcb_pixel = kcb[:, i, x]
                # Run the FAO model for this pixel
                odata = run_fao_model(fc_pixel, kcb_pixel, h, weather_data, index, par, airr)
                # Save results for each parameter
                for param, values in odata.items():
                    if param in results:
                        for date, value in values.items():
                            if date not in results[param]:
                                results[param][date] = np.full((fc.shape[1], fc.shape[2]), np.nan)
                            results[param][date][i, x] = value
            # except Exception as e:
            #     logger.error(f"Error processing pixel ({i}, {x}): {e}")
        logger.info(f"processing pixel ({i}, {x}): Done")    

    # Save all results as rasters
    for param, data_dict in results.items():
        param_output_folder = os.path.join(output_folder, param)
        save_raster(data_dict, param_output_folder, meta, fc.shape[1:])

    logger.info("Field processing completed.")

@shared_task
def fao_model(result, point, field_id):


    ndvi_folder = f"/app/Data/fao_output/{field_id}/ndvi"
    output_folder = f"/app/Data/fao_output/{field_id}"

    files           = [f for f in os.listdir(ndvi_folder) if os.path.isfile(os.path.join(ndvi_folder, f))]
    files           = sorted(files, key=lambda x: x.split('.')[0])
    forcast, dates  = forcast_fao_Open_meteo(point[1], point[0])

    date_range      = pd.date_range(start=files[0].split('.')[0], end=dates[-1], freq='D')
    index           = date_range.strftime('%Y-%j')
    if files[0].split('.')[0] == dates[0]: Weather_Data = forcast
    else :
        Weather_Data    = fao_Open_meteo(forcast,files[0].split('.')[0], date_range[date_range.get_loc(pd.Timestamp(dates[0])) - 1].strftime('%Y-%m-%d'), point[1], point[0])
    weather_data    = Weather(Weather_Data, index)
    par             = Parameters()
    airr            = AutoIrrigate()

    process_field(ndvi_folder, output_folder, weather_data, index, par, airr)

if __name__ == '__main__':
    fao_model('', [-7.678321344603916, 31.66580238055144], 198)