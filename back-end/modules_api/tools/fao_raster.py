from celery import shared_task
import logging
import numpy as np
import os
import rasterio
from rasterio.transform import Affine
from datetime import datetime
import pandas as pd
from pyfao56 import Parameters, Weather, AutoIrrigate, Model, Update, Irrigation
from pyproj import Transformer
from shapely.geometry import mapping
from shapely.ops import transform
from rasterio.mask import mask
from .Open_meteo import fao_Open_meteo, forcast_fao_Open_meteo
from .geoserver_tools import publish_single_layer, create_workspace, delete_workspace
from datetime import date, timedelta, datetime
from rasterio.warp import reproject, Resampling, calculate_default_transform
from shapely.geometry import Polygon, mapping
from shapely.wkt import loads


pd.set_option('display.max_rows', None)  # This will display all rows
pd.set_option('display.max_columns', None)  # This will display all columns



# Initialize logger
logger = logging.getLogger(__name__)


def load_raster_files(folder, polygon, output_folder):
    """Load all NDVI rasters from a folder and return as a list of arrays."""
    files = sorted([f for f in os.listdir(folder) if f.endswith(".tif")], key=lambda x: x.split('.')[0])
    rasters = []
    meta = None

    os.makedirs(f'{output_folder}/ndvi_vis', mode=0o777, exist_ok=True)
    os.chmod(f'{output_folder}/ndvi_vis', 0o777)
    
    for file in files:
            with rasterio.open(os.path.join(folder, file)) as src:
                if meta is None: meta = src.meta.copy()
                ndvi = src.read(1)
                rasters.append(ndvi)  # Read the first band
                output_path = os.path.join(f'{output_folder}/ndvi_vis', f'ndvi_{file}')
                resample_data(meta, ndvi, polygon, ndvi.shape, output_path, f'{output_folder}/ndvi_vis')
    return rasters, meta

def calculate_fc_kcb(ndvis):
    """Calculate FC and Kcb arrays for NDVI rasters."""

    ndvis = np.stack(ndvis)  # Stack into a 3D array (time, height, width)
    
    # nodata_mask = ndvis == -9999
    
    fc = 1.33 * ndvis - 0.20
    kcb = 1.64 * (ndvis - 0.14)

    # Ensure values are non-negative
    fc[fc < 0] = 0
    kcb[kcb < 0] = 0
    
    # fc[nodata_mask] = -9999
    # kcb[nodata_mask] = -9999

    return fc, kcb

def run_fao_model(fc, kcb, h, weather_data, index, par, irr, airr):
    """Run the FAO model for a single pixel."""
    
    data = pd.DataFrame({'fc': fc, 'Kcb': kcb, 'h': h}, index=index)
    update = Update(data)

    model = Model(index[0], index[-1], par, weather_data, autoirr=airr, upd=update, irr=irr)

    model.run()

    return model.odata
def resample_data(meta, data, polygon, shape, output_path, output_folder):

    # print('meta : ', meta)
    # print(polygon, polygon)
    # print('shape', shape)
    polygon = loads(polygon)
    actual_geojson = [mapping(polygon)]
    # print(polygon)
    new_transform, new_width, new_height = calculate_default_transform(
                meta['crs'], meta['crs'], shape[1] * 10, shape[0] * 10,
                *polygon.bounds, resolution=(1, 1)  # Adjust resolution as needed
            )
    # print('new transform : ', new_transform)
    # print('new_width', new_width)
    # print('new_height', new_height)
            # Resample the raster
    resampled_raster = np.empty((new_height, new_width), dtype=meta['dtype'])
    reproject(
        source=data,  # Single-band
        destination=resampled_raster,
        src_transform=meta['transform'],
        src_crs=meta['crs'],
        dst_transform=new_transform,
        dst_crs=meta['crs'],
        resampling=Resampling.bilinear)

    # Clip the resampled raster to the polygon
    with rasterio.MemoryFile() as memfile:
        with memfile.open(
            driver='GTiff',
            height=new_height,
            width=new_width,
            count=1,
            dtype=meta['dtype'],
            crs=meta['crs'],
            transform=new_transform
        ) as dataset:
            dataset.write(resampled_raster, 1)

        with memfile.open() as dataset:
            final_clipped, final_transform = mask(dataset, actual_geojson, crop=True, nodata=np.nan)

    # Update metadata for the clipped raster
    final_meta = meta.copy()
    final_meta.update({
        "transform": final_transform,
        "height": final_clipped.shape[1],
        "width": final_clipped.shape[2],
        "nodata": np.nan,
    })

    # Save the final clipped raster
    # print('before resampling : ',data)
    # print('after resampling : ', final_clipped[0])
    # print('new meta', final_meta)
    with rasterio.open(output_path, 'w', **final_meta) as dst:
        dst.write(final_clipped[0], 1)  # Single-band write
        
    # publish_single_layer(
    #             output_folder.split('/')[-2],
    #             output_path.split('/')[-1],
    #             output_folder.split('/')[-1]
    #         )
def save_raster(data_dict, output_folder, meta, shape, polygon):
    """Save computed rasters to disk."""

    for date_str, data in data_dict.items():
        try:
            # Parse the date
            parsed_date = datetime.strptime(date_str, '%Y-%j')
            date = parsed_date.strftime('%Y-%m-%d')
            output_path = os.path.join(output_folder, f"{output_folder.split('/')[-1]}_{date}.tif")
            # print(data)
            os.makedirs(output_folder, mode=0o777, exist_ok=True)
            os.chmod(output_folder, 0o777)
            
            resample_data(meta, data, polygon, shape, output_path, output_folder)

        except Exception as e:
            print(f"Error processing {date_str}: {e}")
    

def process_field(ndvi_folder, output_folder, weather_data, index, par, airr, polygon, irr):
    """Process NDVI rasters and run the FAO model."""
    logger.info("Starting field processing...")

    # Load NDVI rasters
    ndvis, meta = load_raster_files(ndvi_folder, polygon, output_folder)
    
    len_ndvis, len_index = len(ndvis), len(index)

    while len_ndvis < len_index:
        ndvis.append(ndvis[-1])
        len_ndvis += 1
    
    h = [np.nan] * len(ndvis)

    # Calculate FC and Kcb arrays
    print('start_calculating fc and kcb')
    fc, kcb = calculate_fc_kcb(ndvis)

    # Initialize dictionaries for outputs
    results = {param: {} for param in ['fc', 'Kcb', 'E', 'Zr', 'Ks', 'Kcadj', 'ETcadj', 'T', 'DP', 'Irrig', 'Rain', 'Runoff', 'ETref', 'rzsm_pr']}
    # for param in results:
    #     for date in index:  # Assuming `index` contains all relevant dates
    #         if date not in results[param]:
    #             results[param][date] = np.full((fc.shape[1], fc.shape[2]), -9999, dtype=np.float32)  # Fill with -9999

    for i in range(fc.shape[1]):  # Loop over rows
        for x in range(fc.shape[2]):  # Loop over columns
            try:
                # if not np.any(fc[:, i, x] == -9999) and not np.any(kcb[:, i, x] == -9999):

                fc_pixel = fc[:, i, x]
                kcb_pixel = kcb[:, i, x]
                # Run the FAO model for this pixel
                odata = run_fao_model(fc_pixel, kcb_pixel, h, weather_data, index, par, irr, airr)
                # Save results for each parameter
                for param, values in odata.items():
                    if param in results:
                        for date, value in values.items():
                            if date not in results[param]:
                                results[param][date] = np.full((fc.shape[1], fc.shape[2]), np.nan)
                            results[param][date][i, x] = value
            except Exception as e:
                logger.error(f"Error processing pixel ({i}, {x}): {e}")
        logger.info(f"processing pixel ({i}, {x}): Done")

    # Save all results as rasters
    for param, data_dict in results.items():
        # print(param)
        param_output_folder = os.path.join(output_folder, param)
        save_raster(data_dict, param_output_folder, meta, fc.shape[1:], polygon)
            # break

    logger.info("Field processing completed.")

@shared_task
def fao_model(polygon, point, field_id, irr_data=None):
    
    delete_workspace(field_id)
    create_workspace(field_id)
    ndvi_folder     = f"/app/Data/fao_output/{field_id}/ndvi"
    output_folder   = f"/app/Data/fao_output/{field_id}"

    files           = [f for f in os.listdir(ndvi_folder) if os.path.isfile(os.path.join(ndvi_folder, f))]
    files           = sorted(files, key=lambda x: x.split('.')[0])

    forcast, dates  = forcast_fao_Open_meteo(point[1], point[0])
    yesterday       = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    date_range      = pd.date_range(start=files[0].split('.')[0], end=dates[-1], freq='D')
    index           = date_range.strftime('%Y-%j')
    Weather_Data    = fao_Open_meteo(forcast,files[0].split('.')[0], yesterday, point[1], point[0])
    weather_data    = Weather(Weather_Data, index)
    par             = Parameters()
    airr            = AutoIrrigate()
    if irr_data != None:

        index_len       = len(index)
        irrEff          = [100.0] * index_len
        fw              = [0.3] * index_len
        len_irr         = len(irr_data)
        if index_len    != len(irr_data): irr_data.extend([0] * (index_len - len_irr))

        Data = pd.DataFrame({
            'Depth' : irr_data,
            'fw' : fw,
            'ieff' : irrEff
        }, index=index)

        irr             = Irrigation(Data)
        airr.addset(index[-7], index[-3], ksc=0.9, mad=0.5)
    else : irr = None
    process_field(ndvi_folder, output_folder, weather_data, index, par, airr, polygon, irr)

if __name__ == '__main__':
    irr = [0,0,0,0,22.10251597,0,0,17.68372754,0,0,0,0,0,0,0,0,0,0,0,1.494152744,6.17857993,0,0,0,0,0,0,0,0,0,0,0,0,7.328736828,0,0,0,0,0]
    fao_model([-7.679958, 31.666682], 32, False, irr)