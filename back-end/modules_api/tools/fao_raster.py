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
from Open_meteo import fao_Open_meteo, forcast_fao_Open_meteo
from geoserver_tools import publish_single_layer, create_workspace, delete_workspace
from datetime import date, timedelta, datetime

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
    
    nodata_mask = ndvis == -9999
    
    fc = 1.33 * ndvis - 0.20
    kcb = 1.64 * (ndvis - 0.14)

    # Ensure values are non-negative
    fc[fc < 0] = 0
    kcb[kcb < 0] = 0
    
    fc[nodata_mask] = -9999
    kcb[nodata_mask] = -9999

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
    print('start_calculating fc and kcb')
    fc, kcb = calculate_fc_kcb(ndvis)

    # Initialize dictionaries for outputs
    results = {param: {} for param in ['fc', 'Kcb', 'E', 'Zr', 'Ks', 'Kcadj', 'ETcadj', 'T', 'DP', 'Irrig', 'Rain', 'Runoff', 'ETref']}
    for param in results:
        for date in index:  # Assuming `index` contains all relevant dates
            if date not in results[param]:
                results[param][date] = np.full((fc.shape[1], fc.shape[2]), -9999, dtype=np.float32)  # Fill with -9999

    for i in range(fc.shape[1]):  # Loop over rows
        for x in range(fc.shape[2]):  # Loop over columns
            try:
                if not np.any(fc[:, i, x] == -9999) and not np.any(kcb[:, i, x] == -9999):

                    fc_pixel = fc[:, i, x]
                    kcb_pixel = kcb[:, i, x]
                    # Run the FAO model for this pixel
                    odata = run_fao_model(fc_pixel, kcb_pixel, h, weather_data, index, par, airr)
                    # print(odata['Ks'])
                    # Save results for each parameter
                    for param, values in odata.items():
                        if param in results:
                            for date, value in values.items():
                                results[param][date][i, x] = value
            except Exception as e:
                logger.error(f"Error processing pixel ({i}, {x}): {e}")
        logger.info(f"processing pixel ({i}, {x}): Done")    
    # Save all results as rasters
    for param, data_dict in results.items():
        param_output_folder = os.path.join(output_folder, param)
        save_raster(data_dict, param_output_folder, meta, fc.shape[1:])

    logger.info("Field processing completed.")

@shared_task
def fao_model(result, point, field_id, new_field, irr=None):

    # ndvi_folder = f"/app/Data/fao_output/{field_id}/ndvi"
    output_folder = f"/app/Data/fao_output/{field_id}"
    ndvi_folder = f"/app/Data/test"
    # output_folder = f"/app/Data/fao_output/32"
    # if not new_field:
    #     delete_workspace(field_id)
    #     create_workspace(field_id)
    files           = [f for f in os.listdir(ndvi_folder) if os.path.isfile(os.path.join(ndvi_folder, f))]
    files           = sorted(files, key=lambda x: x.split('.')[0])
    # forcast, dates  = forcast_fao_Open_meteo(point[1], point[0])
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    date_range      = pd.date_range(start=files[0].split('.')[0], end=yesterday, freq='D')
    # index           = date_range.strftime('%Y-%j')
    # if files[0].split('.')[0] == dates[0]: Weather_Data = forcast
    # else :
    #     Weather_Data    = fao_Open_meteo(forcast,files[0].split('.')[0], date_range[date_range.get_loc(pd.Timestamp(dates[0])) - 1].strftime('%Y-%m-%d'), point[1], point[0])
    # weather_data    = Weather(Weather_Data, index)
    # par             = Parameters()
    if irr == None:
        airr            = AutoIrrigate()
    else:
        # index_len = len(index)
        # irrEff = [100.0 * index_len]
        # fw = [0.3] * index_len
        # print(fw)
        pass


    # process_field(ndvi_folder, output_folder, weather_data, index, par, airr)

if __name__ == '__main__':
    irr = []
    fao_model('', [-7.679958, 31.666682], 32, False, 'a')